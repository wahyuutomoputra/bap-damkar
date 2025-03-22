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
                                        {"status": "completed", "total": 10},
                                    ],
                                    "location_summary": [
                                        {"lokasi": "Jakarta", "total": 8},
                                        {"lokasi": "Surabaya", "total": 7},
                                    ],
                                    "monthly_summary": [
                                        {"month": "2024-03", "total": 15},
                                        {"month": "2024-02", "total": 12},
                                    ],
                                },
                            }
                        }
                    },
                }
            },
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
                                        {"jenis": "penyelamatan", "total": 5},
                                    ],
                                    "monthly_summary": [
                                        {"month": "2024-03", "total": 13},
                                        {"month": "2024-02", "total": 10},
                                    ],
                                },
                            }
                        }
                    },
                }
            },
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
                                    "weekly_rescue": 15,
                                },
                            }
                        }
                    },
                }
            },
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
                                        {"date": "2024-03-21", "total": 3},
                                    ]
                                },
                            }
                        }
                    },
                }
            },
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
                                        {"date": "2024-03-21", "total": 2},
                                    ]
                                },
                            }
                        }
                    },
                }
            },
        }
    },
    "/api/report/dashboard/monthly": {
        "get": {
            "summary": "Get monthly dashboard summary",
            "description": "Get comprehensive monthly summary combining rescue and berita acara data",
            "tags": ["Reports"],
            "parameters": [
                {
                    "name": "year",
                    "in": "query",
                    "description": "Year to get summary for (default: current year)",
                    "required": False,
                    "schema": {"type": "integer"},
                },
                {
                    "name": "month",
                    "in": "query",
                    "description": "Month to get summary for (1-12, default: current month)",
                    "required": False,
                    "schema": {"type": "integer", "minimum": 1, "maximum": 12},
                },
            ],
            "responses": {
                "200": {
                    "description": "Successfully retrieved monthly dashboard summary",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "message": "Berhasil mengambil ringkasan dashboard bulanan",
                                "data": {
                                    "period": {
                                        "year": 2024,
                                        "month": 3,
                                        "start_date": "2024-03-01",
                                        "end_date": "2024-03-31",
                                    },
                                    "rescue": {
                                        "summary": {
                                            "total_rescue": 10,
                                            "total_luka": 5,
                                            "total_meninggal": 1,
                                            "rata_rata_respon": "00:15:30",
                                        },
                                        "by_type": [
                                            {"jenis": "Kebakaran", "total": 5},
                                            {"jenis": "Kecelakaan", "total": 3},
                                            {"jenis": "Lainnya", "total": 2},
                                        ],
                                        "by_location": [
                                            {"lokasi": "Jakarta", "total": 6},
                                            {"lokasi": "Bekasi", "total": 4},
                                        ],
                                        "daily_breakdown": [
                                            {"day": 1, "total": 2},
                                            {"day": 2, "total": 1},
                                        ],
                                    },
                                    "berita_acara": {
                                        "summary": {
                                            "total_kejadian": 15,
                                            "rata_rata_respon": "00:10:45",
                                            "respon_tercepat": "00:05:30",
                                            "respon_terlambat": "00:20:15",
                                        },
                                        "by_type": [
                                            {"jenis": "Rumah", "total": 8},
                                            {"jenis": "Gedung", "total": 5},
                                            {"jenis": "Lainnya", "total": 2},
                                        ],
                                        "daily_breakdown": [
                                            {"day": 1, "total": 3},
                                            {"day": 2, "total": 2},
                                        ],
                                    },
                                },
                            }
                        }
                    },
                },
                "400": {
                    "description": "Invalid month value",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "error",
                                "message": "Bulan harus antara 1 dan 12",
                                "errors": "Invalid month value",
                            }
                        }
                    },
                },
            },
        }
    },
}
