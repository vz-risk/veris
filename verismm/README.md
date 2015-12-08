# Vocabulary for Event Recording and Incident Sharing Maturity Model
Vocabulary for Event Recording and Incident Sharing Maturity Model (VERISMM) represents an organizations maturity in recording VERIS incidents.  Different skills are defined based on the VERIS fields collected.  Levels of maturity are defined based on the skills an organization can demonstrate.

Skills and Levels are temporally based.  An organization may be VERIS Maturity Level 3 when an entire year is considered, but only Level 2 during stretches of that year.  Also, an organization may be Level 3 one year, and regress to Level 2 the next.

# Benefits 
VERIS is a tested method for recording events and sharing incidents in such a way as to facilitate useful analysis.  However, recording all of the enumerations available in VERIS can be daunting.  VERISMM provides a means of implementing VERIS incrementally.  It also helps ensure that, as you mature in your implementation of VERIS, you do not focus too much on a single characteristic of your incidents and instead produce well-rounded incident analysis at every level of maturity.

## Basic Level Description
* Level 1: Where everyone starts.  You know that incidents occurred but not much more.
* Level 2: You understand the basics of incidents.  Organizations reaching Level 2 can go to bed knowing they are capturing a holistic, if basic, view of incidents in their organization.  This is a good initial goal for organizations starting with VERIS.
* Level 3: You understand some incident details.  The primary benefit of Level 3 is that provides the ability for the organization to identify the Incident Patterns, (See the 2014 and 2015 DBIR for details on the patterns), that affect their organization.  It also allows organizations to develop attack graphs for themselves rather than relying on general attack graphs developed from the DBIR.  Organizations using VERIS should be able to mature to this level.
* Level 4: You understand most incident details. This is the lowest level that the DBIR team codes incidents in.  This is a reasonable level of incident recording and sharing to maintain without feeling the need to continue improving.  This level is a comfortable level for organizations using VERIS to maintain.
* Level 5: You understand the basic impact of incidents and ancillary details.  This marks a transition from  focusing on the security issues associated with incidents to the business impacts.  Many times this data is simply not available until well after an incident requiring analysts to go back to historic incidents to update them.
* Level 6: You can quantify the impact of incidents.   You record notes on aspects of the incident.
* Level 7: You understand controls in context of your incidents.  You can associate incidents and their impacts with vulnerabilities that allowed the incident to occur and what mitigations should be added to prevent reoccurrence.  You record detailed notes on the aspects of the incident.

## Conducting Analysis
The DBIR team is working hard to provide tools that will allow organizations obtaining certain VERISMM skill and level requirements to produce analysis of their own data comparable to the DBIR as well as to compare their data to the DBIR.

In the mean time, pivot tables in Excel provide a quick an easy way to produce analysis.  The simplest method is to create a pivot table from a spreadsheet of VERIS data and drag the same enumeration into the "row" and "value" box in the pivot table dialog box.  You can then select the data in the pivot table and create a BAR chart based on the data.

If you want to get fancy, try dragging the "data disclosure" into the "filter" field and choose "Yes" from the dropdown that now appears above the pivot table.  Now you are looking at breaches rather than all incidents.

And to get real fancy, drag a different enumeration into the "columns" section of the pivot table.  Now you can see how things affect each other, such as how different actions (the VERIS term for what the threat actor did) affect the discovery method.

# Technical Usage

### Skills
Skills define a set of VERIS enumerations that must be collected to obtain the skill.  When an enumeration lists one or more specific skills, only those specific values of the enumeration are part of the skill.  When "None" or "null" is indicated, all potential values of the enumeration are part of the skill.  

All prior skills must be obtained prior to attempting to obtain a skill.

Each skill lists a "Coverage" value which represents the decimal percentage of the potential enumeration & associated values that an organization must be capable of capturing to be considered as having obtained the skill.  

Additionally, the skill has not been obtained until enough incidents have been captured (after having become capable of obtaining the skill) to identify statistically significant differences in enumerations.  A target of *45* incidents is reasonable.

### Levels
Levels are defined in terms of multiple skills and their associated predecessor skills.  To be capable of obtaining a level, all skills within the level must be obtained.  Enough records must be obtained in the level to see statistically significant differences.  A target of *45* records is a good target.


### Generating Human Readable Text
A simplified, human-readable version of the maturity model can be generated by using the included viersmm_to_markdown.py script:

`python ./convert_to_markdown.py > verismm_levels.md`

The file has helpfully been generated and included in the repository.  Only basic information is included in the markdown file.  For all details of a given skill, see the full json file.