"""
Lab Validation Engine
======================
Backend validation for answers, flags, and other submission types.
Supports: ANSWER_MATCH, REGEX, FLAG_MATCH, MULTI_ANSWER.
Flags are NEVER exposed to the frontend.
"""

import re
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of a validation check."""
    def __init__(self, correct=False, message='', explanation='', xp=0):
        self.correct = correct
        self.message = message
        self.explanation = explanation
        self.xp = xp

    def to_dict(self):
        return {
            'correct': self.correct,
            'message': self.message,
            'explanation': self.explanation if self.correct else '',
            'xp': self.xp,
        }


class ValidationEngine:
    """Backend validation for lab submissions."""

    @staticmethod
    def validate_answer(submission, question):
        """Validate a learner's answer against the question's expected answer.
        
        Args:
            submission: The answer string submitted by the learner.
            question: UploadedLabQuestion model instance.
            
        Returns:
            ValidationResult
        """
        if not submission or not submission.strip():
            return ValidationResult(False, 'Please provide an answer.')

        answer = submission.strip()
        v_type = question.validation_type or 'ANSWER_MATCH'
        expected = question.expected_answer or ''

        if v_type == 'ANSWER_MATCH':
            return ValidationEngine._match_answer(answer, expected, question.case_sensitive)
        elif v_type == 'REGEX':
            return ValidationEngine._regex_match(answer, expected)
        elif v_type == 'MULTI_ANSWER':
            return ValidationEngine._multi_answer(answer, expected, question.case_sensitive)
        else:
            # Default to answer match
            return ValidationEngine._match_answer(answer, expected, question.case_sensitive)

    @staticmethod
    def validate_flag(submission, flag):
        """Validate a flag submission.
        
        Args:
            submission: The flag string submitted by the learner.
            flag: UploadedLabFlag model instance.
            
        Returns:
            ValidationResult
        """
        if not submission or not submission.strip():
            return ValidationResult(False, 'Please enter a flag.')

        submitted = submission.strip()
        expected = flag.flag_value.strip()

        # Exact match for flags (case-sensitive)
        if submitted == expected:
            return ValidationResult(
                True,
                'Flag accepted! Well done.',
                f'Flag: {expected}',
                flag.points
            )
        else:
            return ValidationResult(False, 'Incorrect flag. Try again.')

    @staticmethod
    def _match_answer(answer, expected, case_sensitive=False):
        """Simple string matching with optional case sensitivity."""
        if not expected:
            return ValidationResult(False, 'No expected answer configured.')

        if case_sensitive:
            match = answer.strip() == expected.strip()
        else:
            match = answer.strip().lower() == expected.strip().lower()

        if match:
            return ValidationResult(True, 'Correct! Well done.')
        else:
            return ValidationResult(False, 'Incorrect answer. Try again.')

    @staticmethod
    def _regex_match(answer, pattern):
        """Regex-based validation."""
        try:
            if re.match(pattern, answer, re.IGNORECASE):
                return ValidationResult(True, 'Correct! Well done.')
            else:
                return ValidationResult(False, 'Incorrect answer. Try again.')
        except re.error as e:
            logger.error(f"Invalid regex pattern '{pattern}': {e}")
            return ValidationResult(False, 'Validation error. Please contact admin.')

    @staticmethod
    def _multi_answer(answer, expected_json, case_sensitive=False):
        """Accept any of multiple valid answers (expected is JSON array)."""
        try:
            if isinstance(expected_json, str):
                valid_answers = json.loads(expected_json)
            else:
                valid_answers = expected_json
        except (json.JSONDecodeError, TypeError):
            # Fallback: treat as single answer
            valid_answers = [expected_json]

        if not isinstance(valid_answers, list):
            valid_answers = [valid_answers]

        submitted = answer.strip()
        for valid in valid_answers:
            valid_str = str(valid).strip()
            if case_sensitive:
                if submitted == valid_str:
                    return ValidationResult(True, 'Correct! Well done.')
            else:
                if submitted.lower() == valid_str.lower():
                    return ValidationResult(True, 'Correct! Well done.')

        return ValidationResult(False, 'Incorrect answer. Try again.')
