import { Component, OnInit } from '@angular/core';

const getYears = () => {
  const from: number = 2021;
  const to: number = new Date().getFullYear();
  if (from == to) {
    return `${from}`;
  } else if (from < to) {
    return `${from} - ${to}`;
  }
  return `2021 - ????`;
};

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent implements OnInit {
  years: string = getYears();

  constructor() {}

  ngOnInit(): void {}
}
