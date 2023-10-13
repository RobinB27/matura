# This file contains the DateHelper class. Since this format of a datetime is used
# many times within the project across different modules, the function was added to this
# utility class so it can easily be added to any module.

from datetime import datetime

class DateHelper:
    
    dateFormat: str = "%Y-%m-%d"
    
    def format(date: datetime) -> str:
        """Converts a datetime to the format used by yFinance

        Args:
            date (datetime): date for conversion

        Returns:
            str: date string in correct format
        """
        return date.strftime(DateHelper.dateFormat)
        