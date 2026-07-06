import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import {
  ChatRequest,
  ChatResponse
} from '../models/chat.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  // FastAPI Backend URL
  private readonly API_URL = 'http://localhost:8000/api/chat';

  constructor(
    private http: HttpClient
  ) {}

  askQuestion(question: string): Observable<ChatResponse> {

    const payload: ChatRequest = {
      question: question
    };

    return this.http.post<ChatResponse>(
      this.API_URL,
      payload
    );

  }

}