# Terms of Use
Verizon grants you a limited, revocable, personal and nontransferable license to use the Verizon Enterprise Risk and Incident Sharing Framework for purposes of collecting, organizing and reporting security incident information for non-commercial purposes.  For purposes of this paragraph, "non-commercial purposes" includes organizing and reporting security incident information according to the framework, whether or not for compensation.  But "non-commercial" does not include any attempt to obtain compensation for providing access to, use of, or rights in the framework. 

#---
https://verisframework.wiki.zoho.com/

# XML notes
## Optional vs. nillable: 
Nill elements should be used in cases where there is no data, where the data is unknown, or where data is not-applicable. Optional elements (elements which can occur zero times) are for the purpose of enabling partial implementations of the schema. An element should occur zero times only if that data was not collected because that part of the schema was not implemented.

## Aggregate types: 
Aggregate types are used to limit the multiplicity of certain relationships in order to satisfy requirements for simplified data collection.  For example, suppose an incident involves two external agents. The motive of one is "fun" and the other is "greed". This is modeled as one External AgentAggregate type with motive "fun" AND motive "greed". See issue # (#TODO: put the issue number here) for more details on this.

## Incident vs. case: 
An incident may belong to only one Victim. Many users will track cases with many victims. These should be modeled as incidents on a victim by victim basis.

# Feedback
We are especially interested in the following feedback.

* If/how you extend the schema to meet your organization's particular use cases.
* How you build your internal repository.
* How you respond to the notes above.  

Contact veris@verizon.com or use github to provide feedback.

# Index

* verisc.xsd - the schema itself
* verisc.uml.pdf - This UML diagram provides a high level view of the structure of the schema. We primarily use this for internal development purposes, but we are providing it here because we think it serves some explanatory function as well.
* verisc.lib.xml - This data supplements the schema with valid elements for a number of the enumerations defined in the xsd.
* bin/verisc.py - python bindings for verisc
