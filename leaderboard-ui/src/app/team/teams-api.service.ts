import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import 'rxjs/add/operator/catch';
import {API_URL} from '../env';
import {ITeam} from './team.model';
import * as request from 'superagent';

@Injectable()
export class TeamsApiService {

  constructor() {
  }

  // GET list of public, future events
  getTeams(): Observable<ITeam[]> {
    return;
  }
}