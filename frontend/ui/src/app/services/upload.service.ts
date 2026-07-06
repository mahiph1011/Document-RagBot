import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  // FastAPI Upload Endpoint
  private readonly API_URL = 'http://localhost:8000/api/upload';

  constructor(
    private http: HttpClient
  ) {}

  uploadDocument(file: File): Observable<any> {

    const formData = new FormData();

    formData.append('file', file);

    return this.http.post<any>(
      this.API_URL,
      formData
    );

  }

}