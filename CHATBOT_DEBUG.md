# Chatbot Debugging on Railway

## Problem
Chatbot works locally but shows error on Railway: "Sorry, I'm having trouble connecting right now."

## Solution Steps

### 1. Set GEMINI_API_KEY on Railway ✅
```
GEMINI_API_KEY=AIzaSyD2XYcghB818uiaKhPjSBrP5dOUUGb34ZQ
```

### 2. Add Logging Configuration ⏳
Need to add at the end of `settings.py`:

```python
# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'reservations': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 3. Check Logs After Deploy
Look for:
- `GEMINI_API_KEY not found` → Key not set
- `API Key found: AIzaSyD2XY...` → Key OK
- `Initializing Gemini` → Model loading
- `ERROR` messages → Specific issue

### 4. Common Issues
- **403 Error**: API key invalid → Generate new key
- **Model not found**: Change to `gemini-1.5-flash`
- **CSRF Error**: Already exempt with `@csrf_exempt`
- **Import Error**: Check `google-generativeai` in requirements.txt
