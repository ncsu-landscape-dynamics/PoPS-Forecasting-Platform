from django.db import models


# Create your models here.

class Organization(models.Model):
    # name
    name = models.CharField(verbose_name = "team member organization", help_text="What is the organization name (e.g. NCSU, APHIS)?", max_length = 150, blank=False)
    
    def __str__(self):
        return str(self.name)

class Department(models.Model):
    # name
    name = models.CharField(verbose_name = "department", help_text="What is the department name (e.g. CGA)?", max_length = 150, blank=False)

    def __str__(self):
        return str(self.name)

class Member(models.Model):
    # name
    first_name = models.CharField(verbose_name = "first name", help_text="What is the team member's first name?", max_length = 150, blank=False, null=True)
    last_name = models.CharField(verbose_name = "last name", help_text="What is the team member's last/family name?", max_length = 150, blank=False, null=True)
    # picture
    picture = models.FileField(verbose_name = "team member's picture", help_text="Upload team member image.",upload_to="team_images", max_length=100, blank=False, null=True)
    # role
    role = models.CharField(verbose_name = "team member role", help_text="What is the team member's role in the project?", max_length = 200, blank=False, null=True)
    # title
    title = models.CharField(verbose_name = "team member title", help_text="What is the team member's title (e.g. Graduate Student, Research Associate, etc.)?", max_length = 100, blank=False, null=True)
    # category
    CATEGORY_CHOICES = (
        ("CURRENT", "Current Member"),
        ("PAST", "Past Member"),
        ("AFFILIATE", "Affiliate"),
    )
    category = models.CharField(verbose_name = "member type", help_text="What is the member's category?", max_length = 20,
                    choices = CATEGORY_CHOICES,
                    default = "CURRENT", blank=False, null=True)
    # department
    department = models.ForeignKey(Department, verbose_name = "department", blank = True, null=True,
        on_delete = models.SET_NULL)
    # organization
    organization = models.ForeignKey(Organization, verbose_name = "organization", blank = False, null=True,
        on_delete = models.SET_NULL)
    # department link(?) 
    link = models.URLField(verbose_name = "team member web page URL", help_text="What is member's web page?", blank=True, null=True)
    # github link(?) 
    github = models.URLField(verbose_name = "team member github URL", help_text="What is member's GitHub URL?", blank=True, null=True)

    def __str__(self):
        return str(self.last_name + ", " + self.first_name)