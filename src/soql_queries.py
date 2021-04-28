student_list_query = """
SELECT 
	Id, 
	Full_Name__c, 
	Site__r.Name,
	HIGH_SCHOOL_GRADUATING_CLASS__c,
    toLabel(College_Track_Status__c)
FROM Contact
WHERE College_Track_Status__c IN ('11a', '18a','12A')
"""
