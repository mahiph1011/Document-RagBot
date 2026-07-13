import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';

import { ChatService } from '../../services/chat.service';
import { UploadService } from '../../services/upload.service';

import { ChatResponse } from '../../models/chat.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,

    MatCardModule,
    MatButtonModule,
    MatInputModule,
    MatDividerModule,
    MatFormFieldModule,
    MatIconModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  // ==========================================
  // Theme
  // ==========================================

  darkMode = false;

  // ==========================================
  // Upload
  // ==========================================

  uploadedFile: File | null = null;

  uploading = false;

  // ==========================================
  // Chat
  // ==========================================

  question = '';

  answer = '';

  loading = false;

  sources: any[] = [];

  chatHistory: any[] = [];

  constructor(
    private chatService: ChatService,
    private uploadService: UploadService
  ) {}

  // ==========================================
  // INITIALIZATION
  // ==========================================

  ngOnInit(): void {

    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {

      this.darkMode = true;

      document.body.classList.add('dark-theme');

    }

  }

  // ==========================================
  // FILE PICKER
  // ==========================================

  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {

      this.uploadedFile = input.files[0];

    }

  }

  // ==========================================
  // DRAG OVER
  // ==========================================

  onDragOver(event: DragEvent): void {

    event.preventDefault();

  }

  // ==========================================
  // DROP FILE
  // ==========================================

  onDrop(event: DragEvent): void {

    event.preventDefault();

    if (event.dataTransfer?.files.length) {

      this.uploadedFile = event.dataTransfer.files[0];

    }

  }

  // ==========================================
  // DOCUMENT UPLOAD
  // ==========================================

  uploadDocument(): void {

    if (!this.uploadedFile) {

      alert('Please select a document first.');

      return;

    }

    this.uploading = true;

    this.uploadService.uploadDocument(
      this.uploadedFile
    ).subscribe({

      next: (response) => {

        console.log(response);

        this.uploading = false;

        alert('Document uploaded successfully.');

      },

      error: (error) => {

        console.error(error);

        this.uploading = false;

        alert('Upload failed.');

      }

    });

  }

  currentQuestion = '';

  // ==========================================
  // CHAT
  // ==========================================

  sendMessage(): void {

    if (!this.question.trim()) {

      return;

    }

    const currentQuestion = this.question;

    this.loading = true;

    this.answer = '';

    this.sources = [];

    this.chatService.askQuestion(
      currentQuestion
    ).subscribe({

      next: (response: ChatResponse) => {

        this.answer = response.answer;

        this.sources = response.sources;

        this.chatHistory.push({

          question: currentQuestion,

          answer: response.answer,

          timestamp: new Date()

        });


        this.currentQuestion = this.question;

        this.question = '';

        this.loading = false;

      },

      error: (error) => {

        console.error(error);

        this.loading = false;

        alert('Unable to reach backend.');

      }

    });

  }

  // ==========================================
  // NEW CHAT
  // ==========================================

  newChat(): void {

    this.question = '';

    this.answer = '';

    this.sources = [];

    this.loading = false;

  }

  // ==========================================
  // THEME TOGGLE
  // ==========================================

  toggleTheme(): void {

    this.darkMode = !this.darkMode;

    if (this.darkMode) {

      document.body.classList.add('dark-theme');

      localStorage.setItem(
        'theme',
        'dark'
      );

    }

    else {

      document.body.classList.remove(
        'dark-theme'
      );

      localStorage.setItem(
        'theme',
        'light'
      );

    }

  }

}