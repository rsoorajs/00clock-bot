from babel import Locale
from bot.action.util.format import UserFormatter, TimeFormatter
from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject


class LogFormatter:
    @staticmethod
    def time_point(time_point: str):
        return FormattedText().normal("Time: {time_point}").start_format().bold(time_point=time_point).end_format()

    @staticmethod
    def user(user: ApiObject):
        formatted_user = FormattedText().normal("From: {user}").start_format()\
            .bold(user=UserFormatter(user).full_format).end_format()
        user_language_code = user.language_code
        if user_language_code:
            formatted_user.concat(
                FormattedText().normal(" ({language_code})").start_format()
                    .bold(language_code=user_language_code).end_format()
            )
        return formatted_user

    @classmethod
    def query(cls, query: str, offset: str):
        formatted_query = FormattedText().normal("Query: {query}").start_format().bold(query=query).end_format()
        formatted_query.concat(cls._offset(offset))
        return formatted_query

    @classmethod
    def query_as_title(cls, query: str, offset: str):
        formatted_query = FormattedText().bold(query)
        formatted_query.concat(cls._offset(offset))
        return formatted_query

    @staticmethod
    def _offset(offset: str):
        formatted_offset = FormattedText()
        if offset:
            formatted_offset.normal(" (offset {offset})").start_format().bold(offset=offset).end_format()
        return formatted_offset

    @staticmethod
    def locale(locale: Locale):
        return FormattedText().normal("Locale: {locale}").start_format().bold(locale=str(locale)).end_format()

    @staticmethod
    def locale_as_title(locale: Locale):
        return FormattedText().bold(str(locale))

    @staticmethod
    def processing_time(processing_seconds: float):
        return FormattedText().normal("Processing time: {processing_time}").start_format()\
            .bold(processing_time=TimeFormatter.format(processing_seconds)).end_format()

    @staticmethod
    def results(results_sent: list, results_found: list):
        return FormattedText().normal("{results_sent} results sent / {results_found} results found")\
            .start_format().bold(results_sent=len(results_sent), results_found=len(results_found)).end_format()

    @staticmethod
    def chosen_zone(chosen_zone_name: str):
        return FormattedText().normal("Chosen zone: {zone_name}")\
            .start_format().bold(zone_name=chosen_zone_name).end_format()

    @staticmethod
    def chosen_zone_as_title(chosen_zone_name: str):
        return FormattedText().bold(chosen_zone_name)

    @staticmethod
    def choosing_time(choosing_seconds: float):
        return FormattedText().normal("Choosing time: {choosing_time}").start_format()\
            .bold(choosing_time=TimeFormatter.format(choosing_seconds)).end_format()

    @staticmethod
    def caching_time(caching_seconds: float):
        return FormattedText().normal("Caching time: {caching_time}").start_format()\
            .bold(caching_time=TimeFormatter.format(caching_seconds)).end_format()

    @staticmethod
    def message(*message_parts: FormattedText):
        return FormattedText().newline().join(message_parts)
