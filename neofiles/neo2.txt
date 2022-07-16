match(t:topic),(c:Company)
where t.comp=c.name
create(c)-[:has_topic]->(t)