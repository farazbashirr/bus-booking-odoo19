# -*- coding: utf-8 -*-
"""Offline FAQ chatbot for the customer portal (Phase 8).

Pure offline implementation - no external AI APIs, no internet access.
It uses scikit-learn TF-IDF vectorizers + cosine similarity to match a
free-text question against the fixed FAQ list in ``data/faq_data.py``.

Retrieval model (fitted once per worker, cached as a singleton):

* one word-level TF-IDF vectorizer (unigrams + bigrams, sublinear tf)
  which captures real vocabulary ("cancel", "refund", "boarding"), and
* one character n-gram TF-IDF vectorizer (char_wb, 3-5) which is robust
  to rephrasing, spelling variants and deleted/added words.

Both are l2-normalised (word weighted 1.0, char weighted 0.8) and stacked
into a single matrix; the user question is vectorized the same way and the
best FAQ is chosen by highest cosine similarity. Combining the two spaces
fixes cases that a single vectorizer fails (e.g. "cancel my reservation and
give money back" vs. the cancellation FAQ, or "book a ticket" vs "make a
booking" which only share character n-grams).

Three separate guards guarantee the bot NEVER invents answers and NEVER
acts on transactional requests:

1. an out-of-domain marker list (weather, jokes, recipes, sports...) ->
   immediate fallback message;
2. a minimum similarity threshold; and
3. a "shared words" check that requires at least one non-trivial word of
   the user question to appear in the matched FAQ question, which kills
   pure character-noise matches while keeping all genuine rephrases.

The scikit-learn import is LAZY so this module (and the rest of the addon)
can still be imported on machines where scikit-learn is missing - in that
case the chatbot replies with a "temporarily unavailable" message.
"""

import logging
import re

from odoo import http

_logger = logging.getLogger(__name__)

#: Message shown when no FAQ question beats the guards.
FALLBACK_MESSAGE = (
    "I'm not sure about that - please contact our support desk "
    "for help, or try rephrasing your question."
)

#: Message shown when scikit-learn is not installed in the Odoo venv.
UNAVAILABLE_MESSAGE = (
    "The support assistant is temporarily unavailable. "
    "Please contact our support desk for help."
)

#: Message shown when the user sends a blank question.
EMPTY_QUESTION_MESSAGE = (
    "Please type your question, for example: How do I book a bus ticket?"
)

#: Minimum cosine similarity for an answer to be returned. Tuned
#: empirically against the 200-entry FAQ list: genuine rephrased
#: questions score well above this (typically 0.31-0.97) while
#: unrelated questions stay far below it or are caught by the
#: out-of-domain markers below.
SIMILARITY_THRESHOLD = 0.31

#: Weight of the character-n-gram TF-IDF block relative to the word
#: block inside the combined feature matrix. Word evidence is trusted
#: more; char evidence helps with spelling and word variants.
CHAR_BLOCK_WEIGHT = 0.8

#: Fixed list of question words that can never be about intercity bus
#: service. If any appears (as a whole word) in the user question, we
#: answer with the fallback message instead of guessing - the bot only
#: answers from the FAQ list. Defence in depth alongside the similarity
#: threshold. Matched as whole words so that, e.g., "rain" does not hit
#: the transport word "train".
OUT_OF_DOMAIN_MARKERS = (
    r"weather", r"climate", r"raining", r"rain", r"joke", r"recipe",
    r"cook", r"dish", r"pasta", r"pizza", r"tea", r"chai", r"movie",
    r"film", r"song", r"music", r"sport", r"cricket", r"match", r"game",
    r"politics", r"election", r"news", r"capital of", r"tallest building",
    r"meaning of",
)
_OUT_OF_DOMAIN_RE = re.compile(
    "|".join(r"\b%s\b" % marker for marker in OUT_OF_DOMAIN_MARKERS),
    re.IGNORECASE,
)


class FaqChatbot:
    """Builds the TF-IDF model once and matches FAQ questions with it."""

    #: Lazy process-wide singleton (one per Odoo worker process).
    _instance = None

    _WORD_RE = re.compile(r"\w+")

    def __init__(self):
        self._faq = []
        self._word_vectorizer = None
        self._char_vectorizer = None
        self._question_matrix = None
        self._cosine_similarity = None
        self._unavailable = True

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            from sklearn.preprocessing import normalize as _normalize
        except ImportError:
            _logger.warning(
                "scikit-learn is not installed in the Odoo Python "
                "environment. The offline FAQ chatbot is disabled until "
                "it is installed: pip install scikit-learn "
                "--break-system-packages  (or equivalent)"
            )
            return

        from ..data import faq_data

        self._faq = list(faq_data.FAQ_DATA)
        self._cosine_similarity = cosine_similarity
        self._normalize = _normalize

        # Word-level TF-IDF: unigrams + bigrams, sublinear term frequency.
        self._word_vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        # Character-level TF-IDF (word boundaries, 3-5 chars): robust to
        # rephrasing, typos and word-form variants.
        self._char_vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            sublinear_tf=True,
        )

        questions = [q for q, _a in self._faq]
        word_matrix = self._normalize(
            self._word_vectorizer.fit_transform(questions))
        char_matrix = self._normalize(
            self._char_vectorizer.fit_transform(questions)) * CHAR_BLOCK_WEIGHT
        from scipy.sparse import hstack
        self._question_matrix = hstack([word_matrix, char_matrix]).tocsr()
        self._unavailable = False
        _logger.info("FAQ chatbot ready: %d questions indexed", len(self._faq))

    @classmethod
    def get_chatbot(cls):
        """Return the cached singleton, building it on first use."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _vectorize_question(self, question):
        from scipy.sparse import hstack
        word_vec = self._normalize(
            self._word_vectorizer.transform([question]))
        char_vec = self._normalize(
            self._char_vectorizer.transform([question])) * CHAR_BLOCK_WEIGHT
        return hstack([word_vec, char_vec]).tocsr()

    def _shared_words(self, question, faq_question):
        """Non-trivial words present in both user question and FAQ question.

        Used as a final guard: a match whose top FAQ shares NO content word
        with the user's question is almost certainly character noise.
        """
        words = set(self._WORD_RE.findall(question.lower())) - {"",
            "the", "a", "an", "is", "are", "am", "be", "of", "to", "in",
            "on", "for", "with", "and", "or", "at", "me", "my", "i", "it",
            "do", "does", "did", "can", "how", "what", "when", "where",
            "why", "who", "please", "want", "need", "get", "have", "has",
        }
        q_words = set(self._WORD_RE.findall(faq_question.lower())) - {
            "the", "a", "an", "is", "are", "am", "be", "of", "to", "in",
            "on", "for", "with", "and", "or", "at", "me", "my", "i", "it",
            "do", "does", "did", "can", "how", "what", "when", "where",
            "why", "who", "please", "want", "need", "get", "have", "has",
        }
        return words & q_words

    def _best_match(self, user_question):
        """Return (question, answer) of the best FAQ match, else None.

        Applies: out-of-domain markers, similarity threshold, and the
        shared-word guard - so only a confident FAQ hit is returned.
        """
        if self._unavailable or self._word_vectorizer is None:
            return None
        question = user_question.strip()
        if _OUT_OF_DOMAIN_RE.search(question):
            return None
        try:
            question_vector = self._vectorize_question(question)
        except Exception:
            _logger.exception("Failed to vectorize user question")
            return None
        scores = self._cosine_similarity(
            question_vector, self._question_matrix)[0]
        best_index = int(scores.argmax())
        best_score = float(scores[best_index])
        if best_score < SIMILARITY_THRESHOLD:
            return None
        match = self._faq[best_index]
        if not self._shared_words(question, match[0]):
            return None
        return match

    def get_answer(self, user_question):
        """Return the FAQ answer for a user question (never generated)."""
        if not isinstance(user_question, str):
            user_question = ""
        question = user_question.strip()
        if not question:
            return EMPTY_QUESTION_MESSAGE
        if self._unavailable:
            return UNAVAILABLE_MESSAGE
        match = self._best_match(question)
        if match is None:
            return FALLBACK_MESSAGE
        return match[1]


class BusChatbotController(http.Controller):

    # ------------------------------------------------------------------
    # POST /bus/chatbot/ask — JSON endpoint used by the chat widget.
    # Answers ONLY from the fixed FAQ list or the fallback message; it
    # never performs bookings or any transactional action.
    # ------------------------------------------------------------------
    @http.route('/bus/chatbot/ask', type='jsonrpc', auth='public',
                csrf=False, methods=['POST'])
    def chatbot_ask(self, **kwargs):
        question = kwargs.get('question')
        if not isinstance(question, str):
            question = ''
        answer = FaqChatbot.get_chatbot().get_answer(question)
        return {'answer': answer}