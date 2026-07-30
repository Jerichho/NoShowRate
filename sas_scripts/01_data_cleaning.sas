/* Data Cleaning Script for Airline No-Show Prediction */
/* Author: [Your Name] */
/* Date: [Current Date] */

/* Set up logging */
options mprint mlogic symbolgen;
filename logfile "data_cleaning.log";
proc printto log=logfile new;
run;

/* Create necessary directories */
%macro create_dirs;
    %if not %sysfunc(fileexist(../data/processed)) %then %do;
        x "mkdir -p ../data/processed";
    %end;
    %if not %sysfunc(fileexist(../data/interim)) %then %do;
        x "mkdir -p ../data/interim";
    %end;
%mend;

%create_dirs;

/* Import raw data */
proc import datafile="../data/raw/airline_data.csv"
    out=raw_data
    dbms=csv
    replace;
    guessingrows=max;
run;

/* Log the number of observations and variables */
proc contents data=raw_data out=contents noprint;
run;

proc print data=contents;
    var name type length format informat label;
run;

/* Handle missing values */
data cleaned_data;
    set raw_data;
    
    /* Numeric variables - replace missing with mean */
    array num_vars[*] _numeric_;
    do i = 1 to dim(num_vars);
        if num_vars[i] = . then do;
            /* Calculate mean for each numeric variable */
            proc means data=raw_data noprint;
                var num_vars[i];
                output out=means mean=mean_value;
            run;
            
            /* Replace missing with mean */
            if mean_value ne . then num_vars[i] = mean_value;
        end;
    end;
    
    /* Character variables - replace missing with mode */
    array char_vars[*] _character_;
    do i = 1 to dim(char_vars);
        if char_vars[i] = '' then do;
            /* Calculate mode for each character variable */
            proc freq data=raw_data noprint;
                tables char_vars[i] / out=freqs;
            run;
            
            /* Get mode */
            proc sort data=freqs;
                by descending count;
            run;
            
            /* Replace missing with mode */
            if count > 0 then char_vars[i] = char_vars[i];
        end;
    end;
    
    drop i;
run;

/* Standardize date formats */
data cleaned_data;
    set cleaned_data;
    
    /* Convert dates to ISO 8601 format (YYYY-MM-DD) */
    if booking_date ne . then
        booking_date = input(put(booking_date, yymmdd10.), yymmdd10.);
    if flight_date ne . then
        flight_date = input(put(flight_date, yymmdd10.), yymmdd10.);
        
    format booking_date flight_date yymmdd10.;
run;

/* Create dummy variables for categorical variables */
proc glmmod data=cleaned_data outdesign=design outparm=parameter;
    class fare_class route customer_type;
    model no_show = fare_class route customer_type;
run;

/* Merge dummy variables with cleaned data */
data final_data;
    merge cleaned_data design;
    by _row_;
run;

/* Save processed data */
proc export data=final_data
    outfile="../data/processed/cleaned_data.csv"
    dbms=csv
    replace;
run;

/* Log completion */
proc printto;
run;

/* Print summary statistics */
proc means data=final_data n nmiss mean std min max;
    var _numeric_;
run;

proc freq data=final_data;
    tables _character_;
run; 