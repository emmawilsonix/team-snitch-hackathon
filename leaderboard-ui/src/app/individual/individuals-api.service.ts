import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {API_URL} from '../env';
import {IIndividual} from './individual.model';

@Injectable()
export class IndividualsApiService {

  constructor(private http: HttpClient) {
  }
}