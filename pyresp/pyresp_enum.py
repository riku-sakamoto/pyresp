from enum import Enum,auto

class ReadableAnalysisType(Enum):
  General = auto(),
  EigenAnalysis = auto(),
  DynamicNonLinearAnalysis = auto()


class StoryCSVContent(Enum):
  Title = auto(),
  Version = auto(),
  InputUnit = auto(),
  OutputUnit = auto(),




