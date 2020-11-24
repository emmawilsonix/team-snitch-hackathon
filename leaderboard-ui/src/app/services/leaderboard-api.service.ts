import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError} from 'rxjs';
import {API_URL} from '../env';
import {IUser, ITeam} from '../models/models';
import { catchError } from 'rxjs/operators';

@Injectable()
export class LeaderboardApiService {

  constructor(private http: HttpClient) {
  }

  /** Function to handle any API errors */
  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // Return an observable with a user-facing error message.
    return throwError(
      'Something bad happened; please try again later.');
  }

  /** GET all test teams */
  public getAllTestTeams(): Observable<ITeam[]> {
    return this.http
      .get<ITeam[]>(`${API_URL}/test/teams`)
      .pipe(
        catchError(this.handleError)
      );
  }

  /** GET all test users */
  public getAllTestUsers(): Observable<IUser[]> {
    return this.http
      .get<IUser[]>(`${API_URL}/test/users`)
      .pipe(
        catchError(this.handleError)
      );
  }
}
