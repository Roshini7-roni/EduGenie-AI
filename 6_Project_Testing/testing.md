\# 6. Project Testing



\## Testing Overview



Testing is performed to verify that the EduGenie application works correctly and that its educational features produce responses for the requested inputs.



\## Testing Objectives



\- Verify API functionality.

\- Verify educational modules.

\- Verify quiz generation.

\- Verify different user inputs.

\- Verify error handling.

\- Verify Gemini API integration.



\## Test Cases



| Test ID | Feature | Test Input | Expected Result |

|---|---|---|---|

| TC01 | Explanation | "What is pollination?" | The system provides an explanation about pollination. |

| TC02 | Q\&A | "Why is photosynthesis important?" | The system provides an answer related to photosynthesis. |

| TC03 | Summary | Educational paragraph | The system generates a concise summary. |

| TC04 | Quiz | Educational topic/content | The system generates quiz questions. |

| TC05 | Learning Path | "Learn Python" | The system generates a structured learning path. |

| TC06 | Learning Level | School / College / Advanced | The explanation is generated according to the selected level. |

| TC07 | Invalid/empty input | Empty input | The application handles the request appropriately. |



\## Existing Automated Tests



The project includes test files for application functionality:



\- `tests/test\_api.py`

\- `tests/test\_quiz\_module.py`



\## Manual Testing



The application is also tested through the web interface by entering different educational topics and questions.



Examples include:



\- Pollination

\- Photosynthesis

\- Python programming

\- Operating systems

\- General educational questions



\## Gemini API Testing



The Gemini API integration is tested to verify that the application can send requests and receive AI-generated responses.



The API key is loaded from the local environment configuration.



\## Test Result



The application is tested across its major educational features to verify that the generated response corresponds to the topic or question provided by the learner.

