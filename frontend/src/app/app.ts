import { Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [FormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('Keystone Greeting App');
  protected name = signal('');
  protected greeting = signal('');
  protected error = signal('');

  private readonly http = inject(HttpClient);

  getGreeting(): void {
    this.error.set('');
    const nameValue = this.name();
    const url = nameValue ? `/api/hello/${nameValue}` : '/api/';
    this.http.get<{ message: string }>(url).subscribe({
      next: (response) => {
        this.greeting.set(response.message);
      },
      error: () => {
        this.error.set('Failed to fetch greeting');
      },
    });
  }
}
