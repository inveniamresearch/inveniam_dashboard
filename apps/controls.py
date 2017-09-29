'''
Created on Aug 27, 2017

@author: chansoul
'''
# flake8: noqa

# In[]:
# Controls for webapp

db_info = {"host":"rds-mysql-inveniamdb.cv6j91mlimom.us-east-1.rds.amazonaws.com",
            "db_user":"inveniamdbadmin",
            "password":"Password123!",
            "name":"inveniamfundsdb_final" 
        }

WELL_STATUSES = {
    "Active" : "PRODUCING",
    "Application Received to Drill Plug Convert" : "Application Received to Drill Plug Convert",
    "CANCELLED" : "CANCELLED",
    "DRILLING COMPLETED" : "DRILLING COMPLETED",
    "DRILLED DEEPER" : "DRILLED DEEPER",
    "DRILLING IN PROGRESS" : "DRILLING IN PROGRESS",
    "EXPIRED PERMIT" : "EXPIRED PERMIT",
    "INACTIVE" : "INACTIVE",
    "NOT REPORTED ON AWR" : "NOT REPORTED ON AWR",
    "PLUGGED AND ABANDONED" : "PLUGGED AND ABANDONED",
    "PERMIT ISSUED" : "PERMIT ISSUED",
    "PLUGGED BACK" : "PLUGGED BACK",
    "PLUGGED BACK MULTILATERAL": "PLUGGED BACK MULTILATERAL",
    "REFUNDED FEE" : "REFUNDED FEE",
    "RELEASED WATER WELL" : "RELEASED WATER WELL",
    "SHUT IN" : "SHUT IN",
    "TEMPORARILY ABANDONED" : "TEMPORARILY ABANDONED",
    "TRASNFERRED PERMIT" : "TRASNFERRED PERMIT",
    'UNKNOWN' : 'UNKNOWN',
    'UNKNOWN LOCATED' : 'UNKNOWN LOCATED',
    'UNKNOWN NOT FOUND' : 'UNKNOWN NOT FOUND',
    'Voided Permit' : 'Voided Permit',
    "PRODUCING":"PRODUCING"
}

WELL_TYPES = {
     "BRINE" : "BRINE",
     "CONFIDENTIAL" : "CONFIDENTIAL",
     "DRY HOLE" : 'DRY HOLE',
     "DISPOSAL" : 'DISPOSAL',
     "GAS":"GAS",
     "OIL":"OIL",
     "OIL AND GAS":"OIL AND GAS",
     "PLUGGED AND ABANDONED":"PLUGGED AND ABANDONED",
     "PERMIT":"PERMIT",
     "DRY WILDCAT" : "DRY WILDCAT",
     "GAS DEVELOPMENT" : "GAS DEVELOPMENT",
     "GAS EXTENSION" : "GAS EXTENSION",
     "GAS WILDCAT" : "GAS WILDCAT",
     "GAS INJECTION" : "GAS INJECTION",
     "OIL INJECTION" : "OIL INJECTION",
     "LIQUEFIED PETROLEUM GAS STORAGE" : "LIQUEFIED PETROLEUM GAS STORAGE",
     "MONITORING BRINE" : "MONITORING BRINE",
     "MONITORING MISCELLANEOUS" : 'Monitoring Miscellaneous',
     "MONITORING STORAGE": "MONITORING STORAGE",
     "NOT LISTED" : "NOT LISTED",
     "OBSERVATION WELL" : "OBSERVATION WELL",
     "OIL DEVELOPMENT" : "OIL DEVELOPMENT",
     "OIL EXTENSION" : "OIL EXTENSION",
     "OIL WILDCAT" : "OIL WILDCAT",
     "STRATIGRAPHIC" : "STRATIGRAPHIC",
     "STORAGE" : "STORAGE",
     "GEOTHERMAL" : "GEOTHERMAL",
     "UNKNOWN": "UNKNOWN",
}

WELL_COLORS = {
     "GAS":'#83f442',
     "OIL":'#f48f41',
     "OIL AND GAS":'#c607b6',
     "PLUGGED AND ABANDONED":'#e2041e',
     "PERMIT":'#41f4d3',
     "GAS DEVELOPMENT" : '#FFEDA0',
     "GAS EXTENSION" : '#FA9FB5',
     "GAS WILDCAT" : '#A1D99B',
     "GAS INJECTION" : '#67BD65',
     "OIL DEVELOPMENT" : '#BFD3E6',
     "OIL EXTENSION" : '#B3DE69',
     "OIL WILDCAT" : '#FDBF6F',
     "STORAGE" : '#FC9272',
     "BRINE" : '#D0D1E6',
     "MONITORING BRINE" : '#ABD9E9',
     "OIL INJECTION" : '#3690C0',
     "LIQUEFIED PETROLEUM GAS STORAGE" : '#F87A72',
     "MONITORING STORAGE" : '#CA6BCC',
     "CONFIDENTIAL" : '#DD3497',
     "DRY HOLE" : '#4EB3D3',
     "DISPOSAL" : '#FFFF33',
     "DRY WILDCAT" : '#FB9A99',
     "MONITORING MISCELLANEOUS" : '#A6D853',
     "NOT LISTED" : '#D4B9DA',
     "OBSERVATION WELL" : '#AEB0B8',
     "STRATIGRAPHIC" : '#CCCCCC',
     "GEOTHERMAL" : '#EAE5D9',
     "UNKNOWN" : '#C29A84',
}


query2 = '''
            select API as "API Well Number",
            gas as "Gas Produced, MCF",
            oil as "Oil Produced, bbl" ,
            water as "Water Produced, bbl",
            Year as "Reporting Year"
            from 
            (SELECT PK_Well,API,Well_ID,Well_Name FROM dim_well) as dim_well_info
            inner join 
            (select FK_Well,gas,oil,water,FK_date from fact_production) as fact_prod 
            on
            fact_prod.FK_well=dim_well_info.PK_well
            inner join 
            (SELECT PK_Date,Year FROM inveniamfundsdb_final.dim_date) as dim_date_info
            on
            dim_date_info.PK_Date=fact_prod.FK_date
            '''

query1= '''
        select API as "API Well Number",
        County,
        Operator_Name as "Company Name",
        0 as "API Hole Number",
        0 as "Sidetrack Code" ,
        0 as "Completion Code",
        Well_Type as "Well_Type", 
        Field as "Production Field", 
        Well_Status as "Well_Status",
        Well_Name as "Well Name",
        "" as Town, 
        Producing_Formation as "Producing Formation",
        IFNULL(TOTALPRODUCINGMONTHS,0) as "Months in Production", 
        gas "Gas Produced, MCF",
        oil as "Oil Produced, bbl" ,
        water as "Water Produced, bbl",
        Year as "Reporting Year",
        location as "Location 1"
        from 
        (select FK_Well,FK_Location,Well_Type,Well_Status,Field,Producing_Formation,Cumulative_Water_Production,
        Cumulative_Gas_Production,Cumulative_Oil_Production,FK_Last_Prod_Date,FK_Operator_Current from fact_well_headings) as fct_hdng 
        left join 
        (SELECT FK_Well,TOTALPRODUCINGMONTHS FROM inveniamfundsdb_final.fact_production_summary) as prod_sum
        on prod_sum.FK_Well=fct_hdng.FK_Well
        inner join 
        (select PK_Location,COUNTY as County,concat(STATE,",",COUNTY) as location from dim_location) as dim_loc 
        on dim_loc.PK_Location = fct_hdng.FK_Location 
        inner join
        (SELECT PK_Well,API,Well_ID,Well_Name FROM dim_well) as dim_well_info on fct_hdng.FK_Well=dim_well_info.PK_Well 
        inner join
        (SELECT PK_Operator,Operator_Name FROM inveniamfundsdb_final.dim_operator) as dim_op
        on dim_op.PK_Operator=fct_hdng.FK_Operator_Current
        inner join
        (SELECT PK_Date,Year FROM inveniamfundsdb_final.dim_date) as dim_date_info
        on 
        fct_hdng.FK_Last_Prod_Date=dim_date_info.PK_Date
        inner join
        (select FK_Well,oil,gas,water from fact_production) as fact_prod on fact_prod.FK_well=fct_hdng.FK_Well  

        '''
wellspublic_query = '''
                    select API as "API_WellNo",
                    Well_Name as "Well_Name",
                    Well_Type as "Well_Type",
                    Well_Status as "Well_Status",
                    "SURF" as "Surface_location",
                    completion_date as "Date_Well_Completed",
                    Surface_Longitude as "Surface_Longitude",
                    Surface_Latitude as "Surface_latitude",
                    "BH" as "Bottom_hole_location",
                    Bottom_Hole_Longitude as "Bottom_hole_longitude" ,
                    Bottom_Hole_Latitude as "Bottom_hole_latitude"
                    from 
                    (select FK_Well,Well_Type,Well_Status,FK_Last_Prod_Date,FK_Spud_date,FK_plug_date,
                    Surface_Latitude,Surface_Longitude,Bottom_Hole_Latitude,Bottom_Hole_Longitude from fact_well_headings) as fct_hdng 
                    inner join 
                    (SELECT PK_Well,API,Well_ID,Well_Name FROM dim_well) as dim_well_info on fct_hdng.FK_Well=dim_well_info.PK_Well 
                    inner join 
                    (SELECT FK_Well,date as completion_date FROM fact_completions
                    inner join dim_date on FK_Completion_Date=PK_Date) as com_dt_info on com_dt_info.FK_Well=fct_hdng.FK_Well
                    '''
wellspublic_query_1='''
                    select API as "API_WellNo",
                    County as Cnty, 
                    Wellbore_Profile as Hole,
                    0 as "SideTrck",
                    0 as "Completion",
                    Well_Name as "Well_Name",
                    Operator_Name as "Company Name",
                    FK_Operator_Current as "Operator_number",
                    Well_Type as "Well_Type",
                    "" as "Map_Symbol",
                    Well_Status as "Well_Status",
                    Date_Status as "Date_Status",
                    submit_date as "Date_Permit_Application",
                    Approve_Date as "Permit_Issued",
                    spud_date as "Date_Spudded",
                    "" as "Date_Total_Depth",
                    completion_date as "Date_Well_Completed",    
                    plug_date as "Date_well_plugged",
                    "" as "Date_well_confidential",    
                    "" as "confid",
                    "" as "Town",
                    "" as "quad",
                    "" as "quadsec",
                    short_name as "Producing_name",
                    formation_name as "Producing_formation",
                    "" as "Financial_security",
                    "" as "Slant",
                    County as "County",
                    "" as "Region",
                    "" as "State_lease",
                    "" as "Proposed_depth",
                    "SURF" as "Surface_location",
                    Surface_Longitude as "Surface_Longitude",
                    Surface_Latitude as "Surface_latitude",
                    "BH" as "Bottom_hole_location",
                    Bottom_Hole_Longitude as "Bottom_hole_longitude" ,
                    Bottom_Hole_Latitude as "Bottom_hole_latitude",
                    True_Vertical_Depth as "True_vertical_depth",
                    0 as "Measured_depth",
                    0 as "Kickoff",
                    Total_Depth as "DrilledDepth",
                    DF_Elevation as "Elevation",
                    Well_type as "Original_well_type",
                    0 as "Permit_Fee",
                    "" as "Objective_formation",
                    "" as "Depth_Fee",
                    "" as "Spacing",
                    "" as "Spacing_Acres",
                    "" as "Integration",
                    "" as "Dt_Hearing",
                    "" as "Dt_Mod",
                    "" as "LINK"
                    from 
                    (select FK_Well,FK_Location,Well_Type,Well_Status,Field,Producing_Formation,
                    Cumulative_Gas_Production,Cumulative_Oil_Production,FK_Last_Prod_Date,FK_Operator_Current,
                    FK_Spud_date,FK_plug_date,True_Vertical_Depth,Total_Depth,DF_Elevation,Wellbore_Profile,
                    Surface_Latitude,Surface_Longitude,Bottom_Hole_Latitude,Bottom_Hole_Longitude from fact_well_headings) as fct_hdng 
                    inner join 
                    (select PK_Location,COUNTY as County,concat(STATE,",",COUNTY) as location from dim_location) as dim_loc 
                    on dim_loc.PK_Location = fct_hdng.FK_Location 
                    inner join
                    (SELECT PK_Well,API,Well_ID,Well_Name FROM dim_well) as dim_well_info on fct_hdng.FK_Well=dim_well_info.PK_Well 
                    inner join
                    (SELECT PK_Operator,Operator_Name FROM dim_operator) as dim_op
                    on dim_op.PK_Operator=fct_hdng.FK_Operator_Current
                    inner join
                    (SELECT PK_Date,Year FROM dim_date) as dim_date_info
                    on 
                    fct_hdng.FK_Last_Prod_Date=dim_date_info.PK_Date
                    inner join 
                    (select  FK_Well,FK_date,date as Date_Status from fact_production inner join dim_date on FK_Date=PK_Date) as prod 
                    on prod.FK_Well=fct_hdng.FK_Well
                    inner join
                    (select  FK_Well,b.Date as Submit_Date,d.Date as Approve_Date from fact_permits a, inveniamfundsdb_final.dim_date b,
                    dim_date d 
                    where a.FK_Submit_Date = b.PK_Date 
                    and a.FK_Approved_Date = d.PK_Date) as fct_permit_date on 
                    fct_permit_date.FK_Well=fct_hdng.FK_Well
                    inner join 
                    (SELECT PK_Date,date as spud_date FROM dim_date) as spud_date_info 
                    on spud_date_info.PK_Date=fct_hdng.FK_Spud_date
                    inner join 
                    (SELECT PK_Date,date as plug_date FROM dim_date) as plug_date_info 
                    on plug_date_info.PK_Date=fct_hdng.FK_Spud_date
                    inner join
                    (SELECT PK_Date,date as total_date FROM dim_date) as total_date_info 
                    on total_date_info.PK_Date=fct_hdng.Total_Depth
                    inner join 
                    (SELECT FK_Well,Name as formation_name,short_name FROM fact_formations) as fct_formation 
                    on fct_formation.FK_Well=fct_hdng.FK_Well
                    inner join
                    (SELECT FK_Well,date as completion_date FROM fact_completions
                    inner join dim_date on FK_Completion_Date=PK_Date) as com_dt_info on com_dt_info.FK_Well=fct_hdng.FK_Well
           '''
           
           
