import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-individual-panel',
  templateUrl: './individual-panel.component.html',
  styleUrls: ['./individual-panel.component.scss']
})
export class IndividualPanelComponent implements OnInit {

  @Input() individual;

  @Input() placement;
  
  constructor() { }

  ngOnInit(): void {
  }

}
