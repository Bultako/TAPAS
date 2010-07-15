from django.db import models
from django.db import connection

class SourceSearch_Receivers(models.Model):

    field_label = models.CharField(max_length=50)

    def __unicode__(self):
        return self.field_label

    class Meta:
        db_table = 'SourceSearch_Receivers'
        verbose_name = 'Receivers in Search Web Interface Form'
        verbose_name_plural = 'Receivers in Search Web Interface Form'

class SourceSearch_Receivers_Rx(models.Model):

    sourcesearch_receivers_id = models.IntegerField()
    strxnames_id = models.IntegerField()

    def __unicode__(self):
        return self.sourcesearch_receivers_id, self.strxnames_id

    class Meta:
        db_table = 'SourceSearch_Receivers_Rx'
        verbose_name = 'Table of equivalence for receivers in Search form'

class SourceSearch(models.Model):

    session_id = models.CharField(max_length=40)
    username = models.CharField(max_length=40, blank=True, null=True)
    source_name = models.CharField("Name", max_length=255, blank=True)
    resolver = models.IntegerField("Resolver", blank=True, null=True)
    ra = models.CharField("RA", max_length=40, blank=True)
    dec = models.CharField("Dec.", max_length=40, blank=True)
    size = models.FloatField("Size", blank=True, null=True)
    opacity = models.FloatField("Opacity", blank=True, null=True)
    frequency_from = models.FloatField(blank=True, null=True)
    frequency_to = models.FloatField(blank=True, null=True)
    velocity_from = models.FloatField(blank=True, null=True)
    velocity_to = models.FloatField(blank=True, null=True)
    line_name = models.CharField("Line Name", max_length=45, blank=True)
    exact_line = models.IntegerField("Exact Line Name Match", blank=True, null=True)
    date_from = models.DateField("From", blank=True, null=True) 
    date_to = models.DateField("To", blank=True, null=True)
    project_id = models.CharField("Project ID", max_length=40, blank=True)
    receivers = models.ManyToManyField(SourceSearch_Receivers, 
                    db_table = "SourceSearch_has_Receivers",
                    verbose_name="Receivers",
                    help_text="Receivers used in observation"
                    ) 
    batchfile = models.FileField(upload_to='upload/%Y/%m/%d', blank=True, null=True)
    timestamp =  models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.session_id

    class Meta:
        db_table = 'SourceSearch'
        verbose_name = 'Source Search Web Interface'    
        verbose_name_plural = 'Source Searches Web Interface'

