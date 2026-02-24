import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import type { WritableSignal } from '@angular/core';
import { App } from './app';

interface AppSignals {
  name: WritableSignal<string>;
  greeting: WritableSignal<string>;
  error: WritableSignal<string>;
}

describe('App', () => {
  let httpTesting: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();

    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('should render title', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Keystone Greeting App');
  });

  it('should call GET /api/ when name is empty and set greeting', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    app.getGreeting();

    const req = httpTesting.expectOne('/api/');
    expect(req.request.method).toBe('GET');
    req.flush({ message: 'Hello World' });

    expect((app as unknown as AppSignals).greeting()).toBe('Hello World');
  });

  it('should call GET /api/hello/{name} when name is set and set greeting', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    (app as unknown as AppSignals).name.set('Alice');

    app.getGreeting();

    const req = httpTesting.expectOne('/api/hello/Alice');
    expect(req.request.method).toBe('GET');
    req.flush({ message: 'Hello Alice' });

    expect((app as unknown as AppSignals).greeting()).toBe('Hello Alice');
  });

  it('should trigger getGreeting on button click', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const spy = vi.spyOn(fixture.componentInstance, 'getGreeting').mockImplementation(vi.fn());
    const compiled = fixture.nativeElement as HTMLElement;
    const button = compiled.querySelector<HTMLButtonElement>('#greetButton');
    expect(button).toBeTruthy();
    button?.click();

    expect(spy).toHaveBeenCalled();
  });

  it('should render greeting result when greeting is set', () => {
    const fixture = TestBed.createComponent(App);
    (fixture.componentInstance as unknown as AppSignals).greeting.set('Hello World');
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const result = compiled.querySelector('#greetingResult');
    expect(result).toBeTruthy();
    expect(result?.textContent).toBe('Hello World');
  });

  it('should not render greeting result when greeting is empty', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const result = compiled.querySelector('#greetingResult');
    expect(result).toBeNull();
  });

  it('should set error signal on HTTP failure', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    app.getGreeting();

    const req = httpTesting.expectOne('/api/');
    req.flush('Server Error', { status: 500, statusText: 'Internal Server Error' });

    expect((app as unknown as AppSignals).error()).toBe('Failed to fetch greeting');
  });

  it('should clear error on new request', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    const signals = app as unknown as AppSignals;
    signals.error.set('Previous error');

    app.getGreeting();

    expect(signals.error()).toBe('');

    const req = httpTesting.expectOne('/api/');
    req.flush({ message: 'Hello World' });
  });

  it('should render error message when error is set', () => {
    const fixture = TestBed.createComponent(App);
    (fixture.componentInstance as unknown as AppSignals).error.set('Something went wrong');
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const errorEl = compiled.querySelector('#errorMessage');
    expect(errorEl).toBeTruthy();
    expect(errorEl?.textContent).toContain('Something went wrong');
  });
});
