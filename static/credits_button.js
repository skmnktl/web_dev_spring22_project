'use strict';

const e = React.createElement;

class CreditsButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'Created by Hardik Ajmani, Kasyap Munukutla, Sam Rodman';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Created by'
    );
  }
}

// Find all DOM containers, and render Like buttons into them.
document.querySelectorAll('.credits_button_container')
  .forEach(domContainer => {
    // Read the comment ID from a data-* attribute.
    const commentID = parseInt(domContainer.dataset.commentid, 10);
    const root = ReactDOM.createRoot(domContainer);
    root.render(
      e(CreditsButton, { commentID: commentID })
    );
  });