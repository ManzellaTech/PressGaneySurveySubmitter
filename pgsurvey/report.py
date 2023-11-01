from pathlib import Path
import pandas as pd
import datetime
from typing import NamedTuple, Optional, Callable

class Column(NamedTuple):
    """Represents a column from the input or output spreadsheet."""
    name: str
    old_name: Optional[str] = None
    source_column_name: Optional[str] = None
    default_value: Optional[str] = None
    max_length: Optional[int] = None
    col_index: Optional[int] = None
    func: Optional[Callable] = None
    drop_column: Optional[bool] = None

class ReportPath:
    """Handle input and output spreadsheets."""
    def __init__(self, project_directory: Path,
                 create_input_directory: bool = True,
                 create_output_directory: bool = True) -> None:
        self.project_directory = project_directory
        self.input_directory = project_directory / Path('input')
        self.output_directory = project_directory / Path('output')
        if create_input_directory:
            self.input_directory.mkdir(exist_ok=True)
        if create_output_directory:
            self.output_directory.mkdir(exist_ok=True)
        self.INPUT_FILE_EXT = '.xlsx'
    
    def get_input_file_path(self, input_file_name: str) -> Path:
        """Get the path for the input .xlsx spreadsheet."""
        if input_file_name.endswith(self.INPUT_FILE_EXT) is False:
            input_file_name += self.INPUT_FILE_EXT 
        input_file = self.input_directory / Path(input_file_name)
        if input_file.exists() is False:
            raise FileNotFoundError
        return input_file

    def get_output_path(self, client_id: str, suffix: str) -> Path:
        """Get the path for a spreadsheet being output."""
        allowed_suffixes = ('.xlsx', '.csv')
        if suffix not in allowed_suffixes:
            raise ValueError('The suffix parameter only accepts file extensions: '
                             f'{", ".join(allowed_suffixes)}')
        today = datetime.date.today()
        output_file_stem = f'{client_id}{today.strftime("%m%d%Y")}'
        return self.output_directory / Path(f'{output_file_stem}{suffix}')


class Report:
    """Handle the parsing and transformation of the input data."""
    def __init__(self, df: pd.DataFrame,
                 columns: list[Column],
                 actions: list[str]) -> None:
        self.df = df
        self.columns = columns
        self.actions = actions

    def save_output_csv(self, output_path: Path) -> None:
        """Output to a .csv file."""
        self.df.to_csv(output_path, index=False, encoding='ascii')

    def save_output_xlsx(self, output_path: Path) -> None:
        """Output to an .xlsx file."""
        self.df.to_excel(output_path, index=False)

    def coerce_all_columns_to_data_type_string(self) -> None:
        """Coerce all columns to data type string."""
        self.df = self.df.astype(str)

    def trim_whitespace_from_all_columns(self) -> None:
        """Trim white-space from all columns."""
        self.df = self.df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    def create_new_columns_from_source_columns(self) -> None:
        """Duplicate a column."""
        for col in self.columns:
            if col.source_column_name is not None:
                self.df[col.name] = self.df[col.source_column_name]

    def rename_column_headers(self) -> None:
        """Rename columns."""
        renamed_columns = {h.old_name: h.name for h in self.columns \
                           if h.name != h.old_name}
        self.df.rename(columns=renamed_columns, inplace=True)

    def run_functions_on_columns(self) -> None:
        """If a function is specified to be run on a column, run the function."""
        for col in self.columns:
            if col.func is not None:
                self.df[col.name] = self.df[col.name].apply(col.func) 

    def add_columns_with_default_values(self) -> None:
        """Add a column and fill with a default value."""
        for col in self.columns:
            if col.default_value is not None:
                self.df[col.name] = col.default_value

    def truncate_columns_longer_than_max_length(self) -> None:
        """If a column is longer than the specified max length, truncate it."""
        for col in self.columns:
            if col.max_length is not None:
                self.df[col.name] = self.df[col.name].str.slice(0,col.max_length)
    
    def sort_column_order(self) -> None:
        """Sort the columns matching the order in the config file."""
        column_order = [h.name for h in self.columns]
        self.df = self.df.reindex(column_order, axis=1)

    def remove_email_if_patient_did_not_opt_in(self,
                                        email_column_name: str = 'Email',
                                        use_email_column_name: str = 'Use Email?',
                                        use_email_negative_value: str = 'n') -> None:
        """If email opt-in was not agreed to by patient then don't include email."""
        self.df[email_column_name].mask(self.df[use_email_column_name] == \
                                        use_email_negative_value, '', inplace=True)
        
    def drop_columns_that_are_not_needed(self) -> None:
        """Drop specified columns."""
        columns_to_drop = []
        for col in self.columns:
            if col.drop_column is True:
                columns_to_drop.append(col.name)
        self.df.drop(columns_to_drop, axis=1, inplace=True)

    def run_actions(self) -> None:
        """Run any functions specified in the config file."""
        mapping: dict[str, Callable] = {
            'coerce_all_columns_to_data_type_string': self.coerce_all_columns_to_data_type_string,
            'trim_whitespace_from_all_columns': self.trim_whitespace_from_all_columns,
            'create_new_columns_from_source_columns': self.create_new_columns_from_source_columns,
            'rename_column_headers': self.rename_column_headers,
            'run_functions_on_columns': self.run_functions_on_columns,
            'add_columns_with_default_values': self.add_columns_with_default_values,
            'truncate_columns_longer_than_max_length': self.truncate_columns_longer_than_max_length,
            'sort_column_order': self.sort_column_order,
            'remove_email_if_patient_did_not_opt_in': self.remove_email_if_patient_did_not_opt_in,
            'drop_columns_that_are_not_needed': self.drop_columns_that_are_not_needed,
        }
        for action_name in self.actions:
            action = mapping[action_name]
            action()
