"""
Swagger documentation for Rescue API
"""

# Request body schema for POST and PUT
rescue_schema = {
    "type": "object",
    "properties": {
        "judul_laporan": {
            "type": "string",
            "example": "Penyelamatan Korban Banjir"
        },
        "informasi_diterima": {
            "type": "string",
            "format": "time",
            "example": "14:30:00",
            "description": "Format: HH:MM:SS"
        },
        "tiba_di_lokasi": {
            "type": "string",
            "format": "time",
            "example": "14:45:00",
            "description": "Format: HH:MM:SS"
        },
        "selesai_pemadaman": {
            "type": "string",
            "format": "time",
            "example": "15:30:00",
            "description": "Format: HH:MM:SS"
        },
        "respon_time": {
            "type": "string",
            "format": "time",
            "example": "00:15:00",
            "description": "Format: HH:MM:SS"
        },
        "hari": {
            "type": "string",
            "example": "Senin"
        },
        "tanggal": {
            "type": "string",
            "format": "date",
            "example": "2024-03-20",
            "description": "Format: YYYY-MM-DD"
        },
        "rt": {
            "type": "string",
            "example": "001"
        },
        "rw": {
            "type": "string",
            "example": "002"
        },
        "kampung": {
            "type": "string",
            "example": "Perumahan X"
        },
        "desa_kelurahan": {
            "type": "string",
            "example": "Kelurahan Y"
        },
        "kecamatan": {
            "type": "string",
            "example": "Kecamatan Z"
        },
        "kabupaten_kota": {
            "type": "string",
            "example": "Kota A"
        },
        "nama_pemilik": {
            "type": "string",
            "example": "John Doe"
        },
        "jumlah_penghuni": {
            "type": "integer",
            "example": 4
        },
        "jenis_evakuasi": {
            "type": "string",
            "example": "Evakuasi Banjir"
        },
        "jenis_penyelamatan": {
            "type": "string",
            "example": "Penyelamatan dari Atap Rumah"
        },
        "korban_luka": {
            "type": "integer",
            "example": 0
        },
        "korban_meninggal": {
            "type": "integer",
            "example": 0
        },
        "jumlah_mobil": {
            "type": "integer",
            "example": 2
        },
        "nomor_polisi": {
            "type": "string",
            "example": "B 1234 CD"
        },
        "jumlah_petugas": {
            "type": "integer",
            "example": 8
        },
        "danru_1": {
            "type": "string",
            "example": "Ahmad"
        },
        "danru_2": {
            "type": "string",
            "example": "Budi"
        },
        "danton_1": {
            "type": "string",
            "example": "Charlie"
        },
        "danton_2": {
            "type": "string",
            "example": "David"
        }
    },
    "required": [
        "judul_laporan",
        "informasi_diterima",
        "tiba_di_lokasi",
        "selesai_pemadaman",
        "respon_time",
        "hari",
        "tanggal"
    ]
}

# API Documentation
rescue_docs = {
    "/rescue": {
        "get": {
            "tags": ["Rescue"],
            "summary": "Get all rescue records",
            "description": "Returns a list of all rescue records",
            "security": [{"bearerAuth": []}],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil mengambil semua data rescue",
                                "data": [rescue_schema["properties"]]
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "tags": ["Rescue"],
            "summary": "Create a new rescue record",
            "description": "Creates a new rescue record",
            "security": [{"bearerAuth": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": rescue_schema
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "Successfully created",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil membuat rescue baru",
                                "data": rescue_schema["properties"]
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
                                "message": "Field judul_laporan harus diisi",
                                "errors": "Missing required field: judul_laporan"
                            }
                        }
                    }
                }
            }
        }
    },
    "/rescue/{id}": {
        "get": {
            "tags": ["Rescue"],
            "summary": "Get a rescue record by ID",
            "description": "Returns a single rescue record",
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "ID of rescue record"
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil mengambil data rescue",
                                "data": rescue_schema["properties"]
                            }
                        }
                    }
                },
                "404": {
                    "description": "Not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Data rescue tidak ditemukan",
                                "errors": "Not found"
                            }
                        }
                    }
                }
            }
        },
        "put": {
            "tags": ["Rescue"],
            "summary": "Update a rescue record",
            "description": "Updates an existing rescue record",
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "ID of rescue record"
                }
            ],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": rescue_schema
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Successfully updated",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil mengupdate rescue",
                                "data": rescue_schema["properties"]
                            }
                        }
                    }
                },
                "404": {
                    "description": "Not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Data rescue tidak ditemukan",
                                "errors": "Not found"
                            }
                        }
                    }
                }
            }
        },
        "delete": {
            "tags": ["Rescue"],
            "summary": "Delete a rescue record",
            "description": "Deletes an existing rescue record",
            "security": [{"bearerAuth": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "ID of rescue record"
                }
            ],
            "responses": {
                "200": {
                    "description": "Successfully deleted",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil menghapus rescue"
                            }
                        }
                    }
                },
                "404": {
                    "description": "Not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": False,
                                "message": "Data rescue tidak ditemukan",
                                "errors": "Not found"
                            }
                        }
                    }
                }
            }
        }
    }
} 