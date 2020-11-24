import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-team-panel',
  templateUrl: './team-panel.component.html',
  styleUrls: ['./team-panel.component.scss']
})
export class TeamPanelComponent implements OnInit {

  @Input() team;

  constructor() { }

  ngOnInit(): void {
  }

}
