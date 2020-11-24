import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TeamLeaderboardComponent } from './team-leaderboard/team-leaderboard.component';
import { IndividualLeaderboardComponent } from './individual-leaderboard/individual-leaderboard.component';
import { TeamPanelComponent } from './team-panel/team-panel.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { IndividualPanelComponent } from './individual-panel/individual-panel.component';

@NgModule({
  declarations: [
    AppComponent,
    TeamLeaderboardComponent,
    IndividualLeaderboardComponent,
    TeamPanelComponent,
    LandingPageComponent,
    IndividualPanelComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatCardModule,
    MatGridListModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
