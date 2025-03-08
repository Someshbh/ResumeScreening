import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { JobDescription } from '../Models/JobDescription';


@Injectable({
  providedIn: 'root' // Makes this service globally available
})
export class MainService {

  private apiUrl = 'http://127.0.0.1:8000/parse_resume/';
     

    constructor(private http: HttpClient) { }

    // submitJobDescription(jobDescription: JobDescription): Observable<any> {
    //   return this.http.post<any>(this.apiUrl, jobDescription);
    // }

    submitJobDescription(formData: FormData): Observable<any> {
      return this.http.post<any>(this.apiUrl, formData);
  }
  

}