const uiSchemas = {
  "verisc": {
    "1.3.1": {
      "ui:order": [
        "incident_id",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      timeline: {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2"
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      action: {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "ui:order": [
            "variety",
            "rating",
            "amount",
            "min_amount",
            "max_amount",
            "*"
          ]
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.2": {
      "timeline": {
        "ui:field": "collapsable",
        "incident": {
          "ui:field": "collapsable2"
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      "action": {
        "ui:field": "collapsable",
        "hacking": {
          "ui:field": "collapsable2"
        },
        "malware": {
          "ui:field": "collapsable2"
        },
        "social": {
          "ui:field": "collapsable2"
        },
        "error": {
          "ui:field": "collapsable2"
        },
        "misuse": {
          "ui:field": "collapsable2"
        },
        "physical": {
          "ui:field": "collapsable2"
        },
        "environmental": {
          "ui:field": "collapsable2"
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "asset": {
        "ui:field": "collapsable"
      },
      "attribute": {
        "ui:field": "collapsable",
        "confidentiality": {
          "ui:field": "collapsable2"
        },
        "integrity": {
          "ui:field": "collapsable2"
        },
        "availability": {
          "ui:field": "collapsable2"
        }
      },
      "victim": {
        "ui:field": "collapsable"
      },
      "impact": {
        "ui:field": "collapsable"
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.3": {
      "ui:order": [
        "incident_id",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "incident": {
          "ui:field": "collapsable2"
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      "action": {
        "ui:field": "collapsable",
        "hacking": {
          "ui:field": "collapsable2"
        },
        "malware": {
          "ui:field": "collapsable2"
        },
        "social": {
          "ui:field": "collapsable2"
        },
        "error": {
          "ui:field": "collapsable2"
        },
        "misuse": {
          "ui:field": "collapsable2"
        },
        "physical": {
          "ui:field": "collapsable2"
        },
        "environmental": {
          "ui:field": "collapsable2"
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "asset": {
        "ui:field": "collapsable"
      },
      "attribute": {
        "ui:field": "collapsable",
        "confidentiality": {
          "ui:field": "collapsable2"
        },
        "integrity": {
          "ui:field": "collapsable2"
        },
        "availability": {
          "ui:field": "collapsable2"
        }
      },
      "victim": {
        "ui:field": "collapsable"
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown",
          "*"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable"
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.4": {
      "ui:order": [
        "incident_id",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "incident": {
          "ui:field": "collapsable2"
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      "action": {
        "ui:field": "collapsable",
        "hacking": {
          "ui:field": "collapsable2"
        },
        "malware": {
          "ui:field": "collapsable2"
        },
        "social": {
          "ui:field": "collapsable2"
        },
        "error": {
          "ui:field": "collapsable2"
        },
        "misuse": {
          "ui:field": "collapsable2"
        },
        "physical": {
          "ui:field": "collapsable2"
        },
        "environmental": {
          "ui:field": "collapsable2"
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "asset": {
        "ui:field": "collapsable"
      },
      "attribute": {
        "ui:field": "collapsable",
        "confidentiality": {
          "ui:field": "collapsable2"
        },
        "integrity": {
          "ui:field": "collapsable2"
        },
        "availability": {
          "ui:field": "collapsable2"
        }
      },
      "victim": {
        "ui:field": "collapsable"
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown",
          "*"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable"
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "2.0": {
      "ui:order": [
        "incident_id",
        "security_incident",
        "reference",
        "summary",
        "incident_timeline",
        "source_id",
        "campaign_id",
        "sequence",
        "targeted",
        "notes",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "*"
      ],
      sequence: {
        items: {
          "ui:order": [
            "confidence",
            "timeline",
            "action",
            "actor",
            "asset",
            "attribute",
            "discovery_method",
            "discovery_notes",
            "victim",
            "control_failure",
            "*"
          ],
          action : {
            "ui:order": [
              "hacking",
              "malware",
              "social",
              "error",
              "misuse",
              "physical",
              "environmental",
              "unknown",
              "*"
            ]
          }
        }
      }
    }
  },
  "dbir": {
    "1.3.1": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "ui:order": [
            "variety",
            "rating",
            "amount",
            "min_amount",
            "max_amount",
            "*"
          ]
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.2": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]

        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "ui:order": [
            "variety",
            "rating",
            "amount",
            "min_amount",
            "max_amount",
            "*"
          ]
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.3": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "hosting",
          "management",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]

        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "ui:order": [
            "variety",
            "rating",
            "amount",
            "min_amount",
            "max_amount",
            "*"
          ]
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.4": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "hosting",
          "management",
          "role",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]

        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "ui:order": [
            "variety",
            "rating",
            "amount",
            "min_amount",
            "max_amount",
            "*"
          ]
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "2.0": {}
  },
  "vzir": {
    "1.3.1": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      timeline: {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      action: {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.2": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "time",
            "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
            "items": {
                "ui:order": [
                    "variety",
                    "amount",
                    "*"
                ]
            }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "partner_data",
            "partner_number",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.3": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "time",
            "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "hosting",
          "management",
          "notes",
          "country",
          "*"
        ],
        "assets": {
            "items": {
                "ui:order": [
                    "variety",
                    "amount",
                    "*"
                ]
            }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.4": {
      "ui:order": [
        "master_id",
        "incident_id",
        "investigator",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "notes",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "time",
            "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "role",
          "hosting",
          "management",
          "notes",
          "country",
          "*"
        ],
        "assets": {
            "items": {
                "ui:order": [
                    "variety",
                    "amount",
                    "*"
                ]
            }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "2.0": {}
  },
  "vcdb": {
    "1.3.1": {
      "ui:order": [
        "master_id",
        "incident_id",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "github",
        "reference",
        "summary",
        "notes",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "plus",
        "cost_corrective_action",
        "control_failure",
        "analysis_status",
        "*"
      ],
      timeline: {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      action: {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "cloud",
          "governance",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.2": {
      "ui:order": [
        "master_id",
        "incident_id",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "github",
        "reference",
        "summary",
        "notes",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "plus",
        "cost_corrective_action",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "cloud",
          "governance",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.3": {
      "ui:order": [
        "master_id",
        "incident_id",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "github",
        "reference",
        "summary",
        "notes",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "plus",
        "cost_corrective_action",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "cloud",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.4": {
      "ui:order": [
        "master_id",
        "incident_id",
        "analyst",
        "analyst_notes",
        "dbir_year",
        "security_incident",
        "github",
        "reference",
        "summary",
        "notes",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "plus",
        "cost_corrective_action",
        "control_failure",
        "analysis_status",
        "*"
      ],
      "timeline": {
        "ui:field": "collapsable",
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "notification",
          "*"
        ],
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
          "year",
          "month",
          "day",
          "time",
          "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "cloud",
          "role",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "2.0": {}
  },
  "other": {
    "1.3.1": {},
    "1.3.2": {},
    "1.3.3": {},
    "1.3.4": {},
    "2.0": {}
  },
  "partner": {
    "1.3.1": {
      "ui:order": [
        "master_id",
        "incident_id",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "campaign_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      timeline: {
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ]
      },
      action: {
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "error": {
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "physical": {
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "*"
          ]
        },
        "environmental": {
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        }
      },
      "actor": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown"
        ],
        "external": {
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "*"
          ]
        }
      },
      "asset": {
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:order": [
          "victim_id",
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      }
    },
    "1.3.2": {
      "ui:order": [
        "master_id",
        "incident_id",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      "timeline": {
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "ui:field": "collapsable",
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "time",
            "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            ""
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "governance",
          "hosting",
          "management",
          "accessibility",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_misuse",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "f500",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.3": {
      "ui:order": [
        "master_id",
        "incident_id",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      "timeline": {
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "ui:field": "collapsable",
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "time",
            "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            ""
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "hosting",
          "management",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "1.3.4": {
      "ui:order": [
        "master_id",
        "incident_id",
        "dbir_year",
        "security_incident",
        "reference",
        "summary",
        "source_id",
        "confidence",
        "timeline",
        "victim",
        "action",
        "actor",
        "asset",
        "attribute",
        "targeted",
        "discovery_method",
        "discovery_notes",
        "value_chain",
        "impact",
        "notes",
        "plus",
        "corrective_action",
        "cost_corrective_action",
        "ioc",
        "control_failure",
        "*"
      ],
      "timeline": {
        "ui:order": [
          "incident",
          "compromise",
          "exfiltration",
          "discovery",
          "containment",
          "*"
        ],
        "ui:field": "collapsable",
        "incident": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "time",
            "*"
          ]
        },
        "compromise": {
          "ui:field": "collapsable2",
        },
        "exfiltration": {
          "ui:field": "collapsable2",
        },
        "discovery": {
          "ui:field": "collapsable2",
        },
        "containment": {
          "ui:field": "collapsable2",
        },
        "notification": {
          "ui:field": "collapsable2",
          "ui:order": [
            "year",
            "month",
            "day",
            "*"
          ]
        }
      },
      "action": {
        "ui:field": "collapsable",
        "ui:order": [
          "hacking",
          "malware",
          "social",
          "error",
          "misuse",
          "physical",
          "environmental",
          "unknown",
          "*"
        ],
        "hacking": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "Infiltrate",
            "Elevate",
            "Exfiltrate",
            "cve",
            "*"
          ]
        },
        "malware": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "name",
            "cve",
            "*"
          ]
        },
        "social": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "target",
            "notes",
            "result",
            "*"
          ]
        },
        "error": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "*"
          ]
        },
        "misuse": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "physical": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "vector",
            "notes",
            "result",
            "*"
          ]
        },
        "environmental": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            ""
          ]
        },
        "unknown": {
          "ui:field": "collapsable2"
        }
      },
      "actor": {
        "ui:field": "collapsable",
        "ui:order": [
          "external",
          "internal",
          "partner",
          "unknown",
          "*"
        ],
        "external": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "notes",
            "country",
            "region",
            "name",
            "*"
          ]
        },
        "internal": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "motive",
            "job_change",
            "notes",
            "*"
          ]
        },
        "partner": {
          "ui:field": "collapsable2",
          "ui:order": [
            "motive",
            "notes",
            "industry",
            "country",
            "region",
            "name",
            "*"
          ]
        }
      },
      "asset": {
        "ui:field": "collapsable",
        "ui:order": [
          "total_amount",
          "assets",
          "asset_os",
          "ownership",
          "cloud",
          "role",
          "hosting",
          "management",
          "notes",
          "country",
          "*"
        ],
        "assets": {
          "items": {
            "ui:order": [
              "variety",
              "amount",
              "*"
            ]
          }
        }
      },
      "attribute": {
        "ui:field": "collapsable",
        "ui:order": [
          "confidentiality",
          "integrity",
          "availability",
          "*"
        ],
        "confidentiality": {
          "ui:field": "collapsable2",
          "ui:order": [
            "data_disclosure",
            "data_total",
            "data",
            "data_victim",
            "state",
            "notes",
            "data_abuse",
            "partner_data",
            "partner_number",
            "credit_monitoring",
            "credit_monitoring_years",
            "*"
          ]
        },
        "integrity": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "notes",
            "*"
          ]
        },
        "availability": {
          "ui:field": "collapsable2",
          "ui:order": [
            "variety",
            "duration",
            "notes",
            "*"
          ]
        }
      },
      "victim": {
        "ui:field": "collapsable",
        "ui:order": [
          "victim_id",
          "employee_count",
          "industry",
          "locations_affected",
          "country",
          "region",
          "state",
          "notes",
          "secondary",
          "revenue",
          "*"
        ]
      },
      "discovery_method": {
        "ui:order": [
          "external",
          "internal",
          "partner",
          "other",
          "unknown"
        ],
        "ui:field": "collapsable",
        "external": {
          "ui:field": "collapsable2"
        },
        "internal": {
          "ui:field": "collapsable2"
        },
        "partner": {
          "ui:field": "collapsable2"
        }
      },
      "value_chain": {
        "ui:order": [
          "development",
          "non-distribution services",
          "targeting",
          "distribution",
          "cash-out",
          "money laundering",
          "*"
        ],
        "ui:field": "collapsable",
        "development": {
          "ui:field": "collapsable2"
        },
        "non-distribution services": {
          "ui:field": "collapsable2"
        },
        "targeting": {
          "ui:field": "collapsable2"
        },
        "distribution": {
          "ui:field": "collapsable2"
        },
        "cash-out": {
          "ui:field": "collapsable2"
        },
        "money laundering": {
          "ui:field": "collapsable2"
        }
      },
      "impact": {
        "ui:field": "collapsable",
        "ui:order": [
          "overall_rating",
          "iso_currency_code",
          "overall_amount",
          "overall_min_amount",
          "overall_max_amount",
          "loss",
          "notes",
          "*"
        ],
        "loss": {
          "items": {
            "ui:order": [
              "variety",
              "rating",
              "amount",
              "min_amount",
              "max_amount",
              "*"
            ]
          }
        }
      },
      "plus": {
        "ui:field": "collapsable"
      }
    },
    "2.0": {}
  }
};

module.exports = uiSchemas;
