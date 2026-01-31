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

  private readonly http = inject(HttpClient);

  getGreeting(): void {
    const nameValue = this.name();
    if (!nameValue) {
      this.http.get<{ message: string }>('/api/').subscribe((response) => {
        this.greeting.set(response.message);
      });
    } else {
      this.http.get<{ message: string }>(`/api/hello/${nameValue}`).subscribe((response) => {
        this.greeting.set(response.message);
      });
    }
  }
}
