
class ObjectStatusChoices(object):
    ACTIVE=0
    DELETED=1
    CHOICES = (
        (DELETED, 'Deleted'),
        (ACTIVE, 'Active')
    )


class QuestionCategoryChoices(object):
    EXERCISE=1
    DAILY_PRACTICE_PROBLEMS=2
    SOLVED_EXAMPLES = 3
    CHOICES = (
        (EXERCISE, 'Exercise'),
        (DAILY_PRACTICE_PROBLEMS, 'Daily Practice Problems'),
        (SOLVED_EXAMPLES,'Solved Examples'),
    )



class QuestionTypeChoices(object):
    MULTIPLE_CHOICE=1
    SINGLE_INTEGER=2
    MULTIPLE_RESPONSE=3
    FILL_IN_THE_BLANK=4
    TRUE_FALSE=5
    SUBJECTIVE=6

    CHOICES = (
        (MULTIPLE_CHOICE, 'Multiple Choice Questions'),
        (SINGLE_INTEGER, 'Single Integer Questions'),
        (MULTIPLE_RESPONSE,'Multiple Response Questions'),
        (FILL_IN_THE_BLANK,'Fill in the Blanks'),
        (TRUE_FALSE,'True False'),
        (SUBJECTIVE,'Subjective')
    )



class TOCLevelChoices(object):
    UNIT=0
    CHAPTER=1
    TOPIC=2
    SUBTOPIC=3

    CHOICES = (
        (UNIT, 'Unit'),
        (CHAPTER, 'Chapter'),
        (TOPIC, 'Topic'),
        (SUBTOPIC,'Subtopic'),
    )



class AssessmentTimedChoices(object):
    NONE = 0
    ON_TOTAL = 1
    ON_QUESTION = 2

    CHOICES = (
        (NONE, 'None'),
        (ON_TOTAL, 'Timed on Total'),
        (ON_QUESTION, 'Timed on Questions'),
    )

class DifficultyLevelChoices(object):
    EASY=0
    MEDIUM=1
    HARD=2
    VERY_HARD=3
    CHOICES  = (
        (EASY, "Easy"),
        (MEDIUM, "Medium"),
        (HARD, "Hard"),
        (VERY_HARD, "Very Hard"),
    )


class AssessmentResultChoices(object):
    NEVER = 0
    EVERY_QUESTION = 1
    ASSESSMENT_PASSING = 2
    ALL_ATTEMPTS = 3
    EVERY_ATTEMPT = 4
    NOT_APPLICABLE = 5

    CHOICES  = (
        (NEVER, "Never"),
        (EVERY_QUESTION, "Every Question"),
        (ASSESSMENT_PASSING, "Assessment Passing"),
        (ALL_ATTEMPTS, "All Attempts"),
        (EVERY_ATTEMPT, "Every Attempt"),
        (NOT_APPLICABLE, "Not Applicable"),
           
    )


class AssessmentSolutionVisibilityChoices(object):
    NEVER = 0
    EVERY_QUESTION = 1
    ASSESSMENT_PASSING = 2
    ALL_ATTEMPTS = 3
    EVERY_ATTEMPT = 4
    DEFAULT_OPEN = 5 #for dpp only
    CHOICES  = (
        (NEVER, "Never"),
        (EVERY_QUESTION, "Every Question"),
        (ASSESSMENT_PASSING, "Assessment Passing"),
        (ALL_ATTEMPTS, "All Attempts"),
        (EVERY_ATTEMPT, "Every Attempt"),
        (DEFAULT_OPEN, "Default Open"),
           
    )




class PublishStatusChoices(object):
    DRAFT=0
    PUBLISHED=1
    CHOICES  = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    )


class StudyMaterialTypeChoices(object):
    NOTES=0
    VIDEO=1
    CHOICES  = (
        (NOTES, "Notes"),
        (VIDEO, "Video"),
    )
class ContentTypeChoices(object):
    STUDY_MATERIAL = 1
    ASSESSMENT=2
    CHOICES  = (
        (STUDY_MATERIAL, "Study Material"),
        (ASSESSMENT, "Assessment"),
    )
class ContentSubtypeChoices(object):
    EXERCISE=1
    DAILY_PRACTICE_PROBLEMS=2
    SOLVED_EXAMPLES = 3
    NOTES=4
    VIDEO=5
    CHOICES = (
        (EXERCISE, 'Exercise'),
        (DAILY_PRACTICE_PROBLEMS, 'Daily Practice Problems'),
        (SOLVED_EXAMPLES,'Solved Examples'),
        (NOTES, "Notes"),
        (VIDEO, "Video"),
    )
class LectureDeliveryStatusChoices(object):
    NOT_STARTED=0
    COMPLETED=1
    NOT_COMPLETED=2
    CHOICES  = (
        (NOT_STARTED, "Not Started"),
        (COMPLETED, "Completed"),
        (NOT_COMPLETED, "Not Completed"),
    )

class ContentMappingLevelChoices(object):
    UNIT=1
    CHAPTER=2
    TOPIC=3
    SUBTOPIC=4
    CLASS = 10
    SUBJECT =20
    CHOICES  = (
        (UNIT, "Unit"),
        (CHAPTER, "Chapter"),
        (TOPIC, "Topic"),
        (SUBTOPIC, "Sub Topic"),
        (CLASS, "Class"),
        (SUBJECT, "Subject"),
    )


    @classmethod
    def get_by_toc_level(cls,toc_level):
        mapping={}
        mapping[TOCLevelChoices.UNIT] = ContentMappingLevelChoices.UNIT
        mapping[TOCLevelChoices.CHAPTER] = ContentMappingLevelChoices.CHAPTER
        mapping[TOCLevelChoices.SUBTOPIC] = ContentMappingLevelChoices.SUBTOPIC
        mapping[TOCLevelChoices.TOPIC] = ContentMappingLevelChoices.TOPIC
        return mapping[toc_level]


class LanguageMediumChoices(object):
    ENGLISH=0
    HINDI=1
    CHOICES  = (
        (ENGLISH, "English"),
        (HINDI, "Published"),
    )

class CscType(object):
    COUNTRY=1
    STATE=2
    CITY=3
    CHOICES = (
        (COUNTRY, "Country"),
        (STATE, "State"),
        (CITY, "City"),
        )
