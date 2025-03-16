"""
Swagger documentation for User API
"""

# Request body schema for register
register_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "example": "johndoe",
            "description": "Username for login"
        },
        "email": {
            "type": "string",
            "format": "email",
            "example": "john@example.com",
            "description": "User's email address"
        },
        "password": {
            "type": "string",
            "format": "password",
            "example": "secretpassword123",
            "description": "User's password"
        }
    },
    "required": ["username", "email", "password"]
}

# Request body schema for login
login_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email",
            "example": "john@example.com",
            "description": "User's email address"
        },
        "password": {
            "type": "string",
            "format": "password",
            "example": "secretpassword123",
            "description": "User's password"
        }
    },
    "required": ["email", "password"]
}

# Response schema for user data
user_response_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "example": 1
        },
        "username": {
            "type": "string",
            "example": "johndoe"
        },
        "email": {
            "type": "string",
            "example": "john@example.com"
        }
    }
}

# API Documentation
user_docs = {
    "/auth/register": {
        "post": {
            "tags": ["Authentication"],
            "summary": "Register a new user",
            "description": "Create a new user account with username, email, and password",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": register_schema
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "User successfully registered",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "User registered successfully",
                                "data": user_response_schema["properties"]
                            }
                        }
                    }
                },
                "400": {
                    "description": "Bad request",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Email already registered",
                                "errors": "Email already exists in the system"
                            }
                        }
                    }
                }
            }
        }
    },
    "/auth/login": {
        "post": {
            "tags": ["Authentication"],
            "summary": "Login user",
            "description": "Login with email and password to get access token",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": login_schema
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Login successful",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Login successful",
                                "data": {
                                    "user": user_response_schema["properties"],
                                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                    "token_type": "Bearer"
                                }
                            }
                        }
                    }
                },
                "401": {
                    "description": "Authentication failed",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Invalid email or password",
                                "errors": "Authentication failed"
                            }
                        }
                    }
                }
            }
        }
    },
    "/users": {
        "get": {
            "tags": ["Users"],
            "summary": "Get all users",
            "description": "Returns a list of all users (requires authentication)",
            "security": [{"bearerAuth": []}],
            "responses": {
                "200": {
                    "description": "List of users retrieved successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Users retrieved successfully",
                                "data": [user_response_schema["properties"]]
                            }
                        }
                    }
                },
                "401": {
                    "description": "Unauthorized",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Unauthorized access",
                                "errors": "Invalid or missing token"
                            }
                        }
                    }
                }
            }
        }
    },
    "/users/{id}": {
        "get": {
            "tags": ["Users"],
            "summary": "Get user by ID",
            "description": "Returns a single user by their ID (requires authentication)",
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "User ID"
                }
            ],
            "responses": {
                "200": {
                    "description": "User found",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "User retrieved successfully",
                                "data": user_response_schema["properties"]
                            }
                        }
                    }
                },
                "404": {
                    "description": "User not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "User not found",
                                "errors": "User with specified ID does not exist"
                            }
                        }
                    }
                }
            }
        },
        "put": {
            "tags": ["Users"],
            "summary": "Update user",
            "description": "Update user information (requires authentication)",
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "User ID"
                }
            ],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "example": "newusername"
                                },
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "example": "newemail@example.com"
                                }
                            }
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "User updated successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "User updated successfully",
                                "data": user_response_schema["properties"]
                            }
                        }
                    }
                }
            }
        },
        "delete": {
            "tags": ["Users"],
            "summary": "Delete user",
            "description": "Delete a user (requires authentication)",
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "User ID"
                }
            ],
            "responses": {
                "200": {
                    "description": "User deleted successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "User deleted successfully"
                            }
                        }
                    }
                }
            }
        }
    }
} 