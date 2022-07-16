match(t:topic),(p:property)
where t.comp=p.company and t.name=p.topic
create(t)-[:has_prop]->(p)