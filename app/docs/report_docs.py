report_docs = {
    "/api/report/rescue/summary": {
        "get": {
            "summary": "Get rescue summary statistics",
            "description": "Retrieve summary statistics for rescue operations including status, location, and monthly counts",
            "tags": ["Reports"],
            "responses": {
                "200": {
                    "description": "Successfully retrieved rescue summary",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "data": {
                                    "status_summary": [
                                        {"status": "active", "total": 5},
                                        {"status": "completed", "total": 10}
                                    ],
                                    "location_summary": [
                                        {"lokasi": "Jakarta", "total": 8},
                                        {"lokasi": "Surabaya", "total": 7}
                                    ],
                                    "monthly_summary": [
                                        {"month": "2024-03", "total": 15},
                                        {"month": "2024-02", "total": 12}
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "/api/report/berita-acara/summary": {
        "get": {
            "summary": "Get berita acara summary statistics",
            "description": "Retrieve summary statistics for berita acara including type and monthly counts",
            "tags": ["Reports"],
            "responses": {
                "200": {
                    "description": "Successfully retrieved berita acara summary",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "data": {
                                    "jenis_summary": [
                                        {"jenis": "kebakaran", "total": 8},
                                        {"jenis": "penyelamatan", "total": 5}
                                    ],
                                    "monthly_summary": [
                                        {"month": "2024-03", "total": 13},
                                        {"month": "2024-02", "total": 10}
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "/api/report/dashboard/summary": {
        "get": {
            "summary": "Get dashboard summary statistics",
            "description": "Retrieve key statistics for the dashboard including today's counts and active rescues",
            "tags": ["Reports"],
            "responses": {
                "200": {
                    "description": "Successfully retrieved dashboard summary",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "data": {
                                    "today_rescue": 3,
                                    "today_berita_acara": 2,
                                    "active_rescue": 5,
                                    "weekly_rescue": 15
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "/api/report/rescue/trend": {
        "get": {
            "summary": "Get rescue operation trends",
            "description": "Retrieve daily trends for rescue operations over the last 30 days",
            "tags": ["Reports"],
            "responses": {
                "200": {
                    "description": "Successfully retrieved rescue trends",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "data": {
                                    "daily_trend": [
                                        {"date": "2024-03-20", "total": 2},
                                        {"date": "2024-03-21", "total": 3}
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "/api/report/berita-acara/trend": {
        "get": {
            "summary": "Get berita acara trends",
            "description": "Retrieve daily trends for berita acara over the last 30 days",
            "tags": ["Reports"],
            "responses": {
                "200": {
                    "description": "Successfully retrieved berita acara trends",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "data": {
                                    "daily_trend": [
                                        {"date": "2024-03-20", "total": 1},
                                        {"date": "2024-03-21", "total": 2}
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
} 