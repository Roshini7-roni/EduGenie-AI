\# 3. Project Design



\## System Architecture



EduGenie follows a modular web application architecture.



```text

User

&#x20; |

&#x20; v

Web Interface

&#x20; |

&#x20; v

FastAPI Application

&#x20; |

&#x20; +-------------------+

&#x20; |                   |

&#x20; v                   v

Educational Modules   Configuration

&#x20; |

&#x20; +---- Explanation

&#x20; +---- Q\&A

&#x20; +---- Summary

&#x20; +---- Quiz

&#x20; +---- Learning Path

&#x20; |

&#x20; v

Gemini API

&#x20; |

&#x20; v

AI Generated Response

&#x20; |

&#x20; v

User Interface

