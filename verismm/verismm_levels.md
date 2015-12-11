Level 1
  * Four A's 1
    * attribute.Unknown: all
    * action.Unknown: all
    * actor.Unknown: all
    * asset.assets.variety: Unknown
  * Incident 1
    * Incident_id: all
    * security_incident: all
    * schema_version: all
  * Timeline 1
    * timeline.incident.month: all
    * timeline.incident.year: all
    * timeline.incident.day: all

Level 2
  * Timeline 2
    * timeline.compromise.unit: all
    * timeline.discovery.unit: all
  * Discovery Method 1
    * discovery_method: some
  * Actor 1
    * actor.partner.variety: Unknown
    * actor.external.variety: Unknown
    * actor.internal.variety: Unknown
  * Asset 1
    * asset.assets.variety: some
  * Action 1
    * action.error.variety: Unknown
    * action.environmental.variety: Unknown
    * action.malware.variety: Unknown
    * action.physical.variety: Unknown
    * action.misuse.variety: Unknown
    * action.hacking.variety: Unknown
    * action.social.variety: Unknown
  * Victim 1
    * victim.employee_count: some
    * victim.industry2: all
    * victim.region: all
  * Attribute 1
    * attribute.confidentiality.data.variety: Unknown
    * attribute.confidentiality.data_disclosure: all
    * attribute.integrity.variety: Unknown
    * attribute.availability.variety: Unknown

Level 3
  * Asset 2
    * asset.assets.variety: all
  * Pattern
    * action.error.variety: some
    * action.hacking.vector: Web application
    * action.malware.vector: Direct install
    * attribute.confidentiality.data.variety: Payment
    * actor.external.motive: Espionage
    * action.malware.variety: all
    * action.physical.variety: some
    * action.misuse.variety: all
    * asset.assets.variety: some
    * action.hacking.variety: DoS
    * actor.external.variety: State-affiliated
  * Victim 2
    * victim.employee_count: all
    * victim.industry: all
    * victim.country: all
  * Discovery Method 2
    * discovery_method: all
  * Attack Graph
    * attribute.integrity.variety: all
    * attribute.confidentiality.data.variety: all
    * action.malware.variety: all
    * action.physical.variety: all
    * action.misuse.variety: all
    * action.malware.vector: all
    * action.hacking.variety: all
    * action.social.variety: all
    * attribute.availability.variety: all
  * Action 2 - Blended
    * action.misuse.variety: all
    * action.social.variety: all
  * Actor 2
    * actor.internal.motive: all
    * actor.partner.motive: all
    * actor.external.motive: all
  * Action 2 - Technical
    * action.hacking.variety: all
    * action.malware.vector: all
    * action.malware.variety: all
  * Attribute 2
    * attribute.confidentiality.data_total: all
    * attribute.confidentiality.data.variety: all
    * attribute.integrity.variety: all
    * attribute.availability.variety: all
  * Targeted 1
    * targeted: all
  * Action 2 - Non-Technical
    * action.error.variety: all
    * action.physical.variety: all
    * action.environmental.variety: all

Level 4
  * Asset 3
    * asset.governance: all
    * asset.assets.amount: all
    * asset.country: all
    * asset.cloud: all
  * Quality 1
    * quality: all
  * Timeline 3
    * timeline.compromise.value: all
    * timeline.exfiltration.value: all
    * timeline.containment.unit: all
    * timeline.exfiltration.unit: all
    * timeline.discovery.value: all
    * timeline.containment.value: all
  * Year to Year 1
    * timeline.incident.year: all
  * Action 3
    * action.physical.vector: all
    * action.error.vector: all
  * Actor 3
    * actor.external.country: all
    * actor.partner.country: all
    * actor.partner.variety: all
    * actor.external.variety: all
    * actor.internal.variety: all
    * actor.internal.country: all
  * Attribute 3
    * attribute.confidentiality.data_victim: all
    * attribute.availability.duration.unit: all
    * attribute.confidentiality.state: all
    * attribute.availability.duration.value: all
  * Action 3 - Blended
    * action.misuse.vector: all
    * action.social.vector: all
  * Action 3 - Technical
    * action.hacking.vector: all

Level 5
  * Actor 4
    * actor.partner.industry2: all
    * actor.partner.region: all
    * actor.internal.job_change: all
    * actor.external.name: all
    * actor.partner.industry: all
    * actor.external.region: all
  * Action 4
    * action.hacking.cve: all
    * action.social.target: all
    * action.malware.cve: all
    * action.malware.name: all
  * Victim 3
    * victim.locations_affected: all
    * victim.state: all
    * victim.revenue.amount: all
    * victim.revenue.iso_currency_code: all
    * victim.secondary.amount: all
  * Impact 1
    * impact.overall_rating: all
    * impact.loss.rating: all
    * impact.loss.variety: all

Level 6
  * Incident 2
    * notes: all
    * discovery_notes: all
    * campaign_id: all
    * reference: all
    * summary: all
  * Four A's 2
    * attribute.unknown.notes: all
    * action.unknown.notes: all
    * actor.unknown.notes: all
    * asset.notes: all
  * Impact 2
    * impact.loss.max_amount: all
    * impact.loss.amount: all
    * impact.loss.min_amount: all
    * impact.iso_currency_code: all

Level 7
  * Actor 5
    * actor.internal.notes: all
    * actor.partner.notes: all
    * actor.external.notes: all
  * Incident 3
    * victim.notes: all
    * victim.secondary.notes: all
    * impact.notes: all
  * Action 5
    * action.error.notes: all
    * action.physical.notes: all
    * action.malware.notes: all
    * action.social.notes: all
    * action.environmental.notes: all
    * action.hacking.notes: all
    * action.misuse.notes: all
  * Controls 1
    * corrective_action: all
    * cost_corrective_action: all
    * control_failure: all
  * Attribute 4
    * attribute.confidentiality.notes: all
    * attribute.availability.notes: all
    * attribute.integrity.notes: all

