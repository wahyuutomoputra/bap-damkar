"""
Swagger documentation for Berita Acara Pemadaman API
"""

# Request body schema for POST and PUT
berita_acara_schema = {
    "type": "object",
    "properties": {
        "judul_laporan": {
            "type": "string",
            "example": "Kebakaran di Perumahan X"
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
        "jenis_bangunan": {
            "type": "string",
            "example": "Rumah Tinggal"
        },
        "area_terbakar": {
            "type": "string",
            "example": "Dapur"
        },
        "luas_area": {
            "type": "integer",
            "example": 20
        },
        "penyebab_kebakaran": {
            "type": "string",
            "example": "Korsleting Listrik"
        },
        "aset_keseluruhan": {
            "type": "number",
            "format": "float",
            "example": 500000000.00
        },
        "nilai_kerugian": {
            "type": "number",
            "format": "float",
            "example": 50000000.00
        },
        "aset_terselamatkan": {
            "type": "number",
            "format": "float",
            "example": 450000000.00
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
berita_acara_docs = {
    "/berita-acara": {
        "get": {
            "tags": ["Berita Acara Pemadaman"],
            "summary": "Get all berita acara pemadaman",
            "description": "Returns a list of all berita acara pemadaman",
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil mengambil semua data berita acara",
                                "data": [berita_acara_schema["properties"]]
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "tags": ["Berita Acara Pemadaman"],
            "summary": "Create a new berita acara pemadaman",
            "description": "Creates a new berita acara pemadaman record",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": berita_acara_schema
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
                                "message": "Berhasil membuat berita acara baru",
                                "data": berita_acara_schema["properties"]
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
    "/berita-acara/{id}": {
        "get": {
            "tags": ["Berita Acara Pemadaman"],
            "summary": "Get a berita acara pemadaman by ID",
            "description": "Returns a single berita acara pemadaman",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "ID of berita acara pemadaman"
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil mengambil data berita acara",
                                "data": berita_acara_schema["properties"]
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
                                "message": "Berita acara dengan id {id} tidak ditemukan",
                                "errors": "Not found"
                            }
                        }
                    }
                }
            }
        },
        "put": {
            "tags": ["Berita Acara Pemadaman"],
            "summary": "Update a berita acara pemadaman",
            "description": "Updates an existing berita acara pemadaman record",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "ID of berita acara pemadaman"
                }
            ],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": berita_acara_schema
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
                                "message": "Berhasil mengupdate berita acara",
                                "data": berita_acara_schema["properties"]
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
                                "message": "Berita acara dengan id {id} tidak ditemukan",
                                "errors": "Not found"
                            }
                        }
                    }
                }
            }
        },
        "delete": {
            "tags": ["Berita Acara Pemadaman"],
            "summary": "Delete a berita acara pemadaman",
            "description": "Deletes an existing berita acara pemadaman record",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "integer"
                    },
                    "description": "ID of berita acara pemadaman"
                }
            ],
            "responses": {
                "200": {
                    "description": "Successfully deleted",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "Berhasil menghapus berita acara"
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
                                "message": "Berita acara dengan id {id} tidak ditemukan",
                                "errors": "Not found"
                            }
                        }
                    }
                }
            }
        }
    }
} 