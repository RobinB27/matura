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
        