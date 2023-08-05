# define CATCH_CONFIG_MAIN
# include "catch.hpp"
# include "csv_parser.hpp"
# include <string>
# include <vector>

using namespace csvmorph;

TEST_CASE( "Test Reading CSV From Direct Input", "[read_csv_direct]" ) {
    std::string csv_string1("123,234,345\r\n"
                            "1,2,3\r\n"
                            "1,2,3");
                            ;
    std::vector<std::string> col_names = {"A", "B", "C"};
    
    // Feed Strings
    CSVReader reader(",", "\"");
    reader.set_col_names(col_names);
    reader.feed(csv_string1);
    reader.end_feed();
    
    // Expected Results
    std::vector<std::string> first_row = {"123", "234", "345"};
    REQUIRE( reader.pop() == first_row );
}

TEST_CASE( "Test Comma Escape", "[read_csv_direct2]" ) {
    std::string csv_string2 = ("123,\"234,345\",456\r\n"
                               "1,2,3\r\n"
                               "1,2,3");
    std::vector<std::string> col_names = {"A", "B", "C"};
    
    // Feed Strings
    CSVReader reader(",", "\"");
    reader.set_col_names(col_names);
    reader.feed(csv_string2);
    reader.end_feed();
    
    // Expected Results
    std::vector<std::string> first_row = {"123", "234,345", "456"};
    REQUIRE( reader.pop() == first_row );
}

TEST_CASE( "Test Read CSV with Header Row", "[read_csv_header]" ) {
    // Header on first row
    CSVReader reader(",", "\"", 0);
    reader.read_csv("./tests/data/real_data/2015_StateDepartment.csv");
    
    // Expected Results
    std::vector<std::string> col_names = {
        "Year", "Entity Type", "Entity Group", "Entity Name",
        "Department / Subdivision", "Position", "Elected Official",
        "Judicial", "Other Positions", "Min Classification Salary",
        "Max Classification Salary", "Reported Base Wage", "Regular Pay",
        "Overtime Pay", "Lump-Sum Pay", "Other Pay", "Total Wages",
        "Defined Benefit Plan Contribution", "Employees Retirement Cost Covered",
        "Deferred Compensation Plan", "Health Dental Vision",
        "Total Retirement and Health Cost", "Pension Formula",
        "Entity URL", "Entity Population", "Last Updated",
        "Entity County", "Special District Activities"
    };
    
    std::vector<std::string> first_row = {
        "2015","State Department","","Administrative Law, Office of","",
        "Assistant Chief Counsel","False","False","","112044","129780",""
        ,"133020.06","0","2551.59","2434.8","138006.45","34128.65","0","0"
        ,"15273.97","49402.62","2.00% @ 55","http://www.spb.ca.gov/","",
        "08/02/2016","",""
    };
    REQUIRE( reader.pop() == first_row );
    REQUIRE( reader.get_col_names() == col_names );
    
    // Can confirm with MS Excel, etc...
    REQUIRE( reader.row_num == 246498 );
}

// std::string psv_string = "123|\"234,345\"|456\r\n1|2|3\r\n1|2|3";