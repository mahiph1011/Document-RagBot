export interface ChatSource {

  document: string;

  section: string;

  similarity: number;

}

export interface ChatResponse {

  question: string;

  answer: string;

  sources: ChatSource[];

}

export interface ChatRequest {

  question: string;

}