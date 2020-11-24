import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ITeam } from '../team/team.model';
import { TeamsApiService } from '../team/teams-api.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css']
})
export class LandingPageComponent implements OnInit {
  private teamsList: ITeam[];

  constructor(private teamsApi: TeamsApiService) {}

  ngOnInit(): void {
    this.getTeams();
  }

  public getTeams(): void {
    this.teamsApi
      .getAllTeams()
      .subscribe(response => {
        this.teamsList = response;
      },
      console.error
    );
  }
}
