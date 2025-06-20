#!/usr/bin/env python3
"""
Logging configuration for the AI Service.
This module provides easy-to-use logging setup functions.
"""

import logging
import sys
from typing import Optional

def setup_logging(level: str = "INFO", 
                  format_string: Optional[str] = None,
                  log_to_file: bool = False,
                  log_file: str = "ai_service.log") -> None:
    """
    Setup logging configuration for the AI Service.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        log_to_file: Whether to log to file in addition to console
        log_file: Name of the log file if log_to_file is True
    """
    
    # Convert string level to logging constant
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    log_level = level_map.get(level.upper(), logging.INFO)
    
    # Default format string
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        print(f"📝 Logging to file: {log_file}")
    
    print(f"🔧 Logging configured: level={level}, log_to_file={log_to_file}")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def set_log_level(level: str) -> None:
    """
    Change the logging level for all loggers.
    
    Args:
        level: New logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    log_level = level_map.get(level.upper(), logging.INFO)
    
    # Set level for root logger
    logging.getLogger().setLevel(log_level)
    
    # Set level for all handlers
    for handler in logging.getLogger().handlers:
        handler.setLevel(log_level)
    
    print(f"🔧 Log level changed to: {level}")

# Predefined logging configurations
def setup_debug_logging():
    """Setup logging for debugging with maximum verbosity."""
    setup_logging(level="DEBUG", log_to_file=True, log_file="ai_service_debug.log")

def setup_production_logging():
    """Setup logging for production with minimal output."""
    setup_logging(level="WARNING", log_to_file=True, log_file="ai_service_production.log")

def setup_development_logging():
    """Setup logging for development with balanced verbosity."""
    setup_logging(level="INFO", log_to_file=True, log_file="ai_service_development.log")

# Auto-setup when imported
if __name__ != "__main__":
    # Default setup - can be overridden by calling setup_logging() explicitly
    setup_logging(level="INFO") 