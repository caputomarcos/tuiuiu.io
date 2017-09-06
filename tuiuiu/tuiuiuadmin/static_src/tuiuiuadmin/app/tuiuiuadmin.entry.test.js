const tuiuiu = require('tuiuiu-client');
tuiuiu.initExplorer = jest.fn();

document.addEventListener = jest.fn();

require('./tuiuiuadmin.entry');

describe('tuiuiuadmin.entry', () => {
  const [event, listener] = document.addEventListener.mock.calls[0];

  it('DOMContentLoaded', () => {
    expect(event).toBe('DOMContentLoaded');
  });

  it('init', () => {
    listener();
    expect(tuiuiu.initExplorer).not.toHaveBeenCalled();
  });

  it('init with DOM', () => {
    document.body.innerHTML = '<div data-explorer-menu></div><div data-explorer-start-page></div>';
    listener();
    expect(tuiuiu.initExplorer).toHaveBeenCalled();
  });
});
