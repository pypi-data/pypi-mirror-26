from __future__ import (absolute_import, division, print_function)

import wof.models as wof_base

class Variable(wof_base.BaseVariable):

    def __init__(self, v=None,
                 VarSampleMedium=None, v_unit=None, v_tunit=None, v_timeinterval=None):
        variable_key = '%s::%s-%s' % (v.VariableCode,
                                      v_unit.UnitsID,
                                      VarSampleMedium)
        self.VariableID = v.VariableID
        self.VariableCode = variable_key
        self.VariableName = v.VariableNameCV
        self.VariableDescription = v.VariableDefinition
        self.NoDataValue = v.NoDataValue
        self.SampleMedium = VarSampleMedium
        self.DataType = v.VariableTypeCV
        self.Speciation = v.SpeciationCV
        self.VariableUnitsID = v_unit.UnitsID
        if v_unit is not None:
            self.VariableUnits = Unit(v_unit)
        else:
            self.VariableUnits = None
        if v_tunit is not None:
            self.TimeUnits = Unit(v_tunit)
            #self.TimeSupport = v_timeinterval
        else:
            self.TimeUnits = None

    #SampleMedium = wof_base.SampleMediumTypes.NOT_RELEVANT
    #ValueType = Column(String)
    #IsRegular = Column(Boolean)
    #TimeSupport = Column(Float)
    #TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    #DataType = Column(String)
    #GeneralCategory = wof_base.GeneralCategoryTypes.WATER_QUALITY

    #VariableUnits = relationship("Units",
    #                    primaryjoin='Variable.VariableUnitsID==Units.UnitsID')

    #TimeUnits = relationship("Units",
    #                    primaryjoin='Variable.TimeUnitsID==Units.UnitsID')

class Site(wof_base.BaseSite):

    def __init__(self, s=None):
        self.SiteID = s.SamplingFeatureID
        self.Latitude = s.Latitude
        self.Longitude = s.Longitude
        self.LatLongDatumID = s.SpatialReferenceID
        self.SiteCode = s.SamplingFeatureCode
        self.SiteName = s.SamplingFeatureName
        self.Elevation_m = s.Elevation_m
        self.Comments = s.SamplingFeatureDescription
        sr = wof_base.BaseSpatialReference()
        sr.SpatialReferenceId = s.SpatialReferenceObj.SpatialReferenceID
        sr.SRSID = s.SpatialReferenceObj.SRSCode
        sr.SRSName = s.SpatialReferenceObj.SRSName
        sr.Notes = s.SpatialReferenceObj.SRSDescription
        self.LatLongDatum = sr

class Series(wof_base.BaseSeries):
    def __init__(self, r=None, aff=None,bdate=None,edate=None):
        fa_obj = r.FeatureActionObj
        u_obj = r.UnitsObj
        v_obj = r.VariableObj
        p_obj = r.ProcessingLevelObj

        sf_obj = fa_obj.SamplingFeatureObj
        a_obj = fa_obj.ActionObj
        m_obj = a_obj.MethodObj
        o_obj = m_obj.OrganizationObj

        self.SeriesID = r.ResultID
        #self.SiteID = fa_obj.SamplingFeatureID
        #self.SiteCode = sf_obj.SamplingFeatureCode
        #self.SiteName = sf_obj.SamplingFeatureName

        self.Variable = Variable(v_obj,
                                 r.SampledMediumCV,
                                 u_obj)
        #self.VariableID = r.VariableID
        #self.VariableCode = v_obj.VariableCode
        #self.VariableName = v_obj.VariableNameCV
        self.SampleMedium = r.SampledMediumCV
        self.QualityControlLevelID = p_obj.ProcessingLevelID
        self.QualityControlLevelCode = p_obj.ProcessingLevelCode
        self.Definition = p_obj.Definition
        self.Explanation = p_obj.Explanation
        #self.MethodID = m_obj.MethodID
        #self.MethodDescription = m_obj.MethodDescription
        self.Method = Method(m_obj)
        self.Organization = o_obj.OrganizationName
        self.BeginDateTimeUTC = bdate.isoformat() #a_obj.BeginDateTime.isoformat()
        if a_obj.EndDateTime is not None:
            self.EndDateTimeUTC = edate.isoformat() #a_obj.EndDateTime.isoformat()
        self.ValueCount = r.ValueCount
        if aff is not None:
            self.Source = Source(aff)

class DataValue(wof_base.BaseDataValue):

    def __init__(self,v,aff_obj=None):
        self.ValueID = v.ValueID
        self.DataValue = v.DataValue
        self.DateTimeUTC = v.ValueDateTime.isoformat()
        self.UTCOffset = v.ValueDateTimeUTCOffset
        if aff_obj is not None:
            self.SourceID = aff_obj.AffiliationID
            #self.SourceCode = aff_obj.OrganizationObj.OrganizationCode

        self.CensorCode = v.ResultObj.CensorCodeCV
        self.MethodID = v.ResultObj.FeatureActionObj.ActionObj.MethodObj.MethodID
        self.QualityControlLevelID = v.ResultObj.ProcessingLevelObj.ProcessingLevelID
        #self.QualityControlLevel = QualityControlLevel(v.ResultObj.ProcessingLevelObj)
        self.QualityControlLevel = v.ResultObj.ProcessingLevelObj.ProcessingLevelCode

        #extra info
        #self.MethodCode = v.ResultObj.FeatureActionObj.ActionObj.MethodObj.MethodCode
        #self.VariableID = v.ResultObj.VariableID
        #self.UnitID = v.ResultObj.UnitsID
        #self.SampleMedium = v.ResultObj.SampledMediumCV

class Method(wof_base.BaseMethod):
    def __init__(self,m_obj):
        self.MethodID = m_obj.MethodID
        self.MethodDescription = m_obj.MethodDescription
        self.MethodLink = m_obj.MethodLink
        self.MethodCode = m_obj.MethodCode

class Unit(wof_base.BaseUnits):
    def __init__(self,u_obj):
        self.UnitsID = u_obj.UnitsID
        self.UnitsName = u_obj.UnitsName
        self.UnitsType = u_obj.UnitsTypeCV
        self.UnitsAbbreviation = u_obj.UnitsAbbreviation

class Source(wof_base.BaseSource):
    def __init__(self,aff_obj):
        self.SourceID = aff_obj.AffiliationID
        self.Organization = aff_obj.OrganizationObj.OrganizationName
        self.OrganizationCode = aff_obj.OrganizationObj.OrganizationCode
        self.SourceCode = aff_obj.OrganizationObj.OrganizationCode
        self.SourceDescription = aff_obj.OrganizationObj.OrganizationDescription
        self.SourceLink = aff_obj.OrganizationObj.OrganizationLink
        self.ContactName = '%s %s' % (aff_obj.PersonObj.PersonFirstName,aff_obj.PersonObj.PersonLastName)
        self.Phone = aff_obj.PrimaryPhone
        self.Email = aff_obj.PrimaryEmail
        self.Address = aff_obj.PrimaryAddress
        #self.City = 'San Diego'
        #self.State = 'CA'
        #self.ZipCode = '92122'

class QualityControlLevel(wof_base.BaseQualityControlLevel):
    def __init__(self, p_obj):
        self.QualityControlLevelID = p_obj.ProcessingLevelID
        self.QualityControlLevelCode = p_obj.ProcessingLevelCode
        self.Definition = p_obj.Definition
        self.Explanation = p_obj.Explanation
