from  parsers import *
from  extractors import *

class BasicProfile:
    def __init__(self,firstName,lastName,occupation,objectUrn,
            entityUrn,publicIdentifier,trackingId,
            backgroundImage=None,**kwargs):

        self.firstName = firstName
        self.lastName = lastName
        self.occupation = occupation
        self.objectUrn = objectUrn
        self.entityUrn = entityUrn
        self.publicIdentifier = publicIdentifier
        self.trackingId = trackingId
        self.objectUrnId = parseUrn(self.objectUrn)[1]
        self.entityUrnId = parseUrn(self.entityUrn)[1]
