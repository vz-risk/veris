import React, { Component } from 'react'
import { 
  Link
} from 'react-router-dom'
import PropTypes from 'prop-types'

export function VzBoxComponent(props) {
  return <div className="box">
      <div className="box-header">
        <h2>{props.title}</h2>
        <div className="clearfix" />
      </div>
      <div className="box-boday">
        {props.children}
      </div>
    </div>;
}

export class VzCollapsible extends Component {
  constructor(props) {
    super(props)

    // Bind class methods
    this.handleTriggerClick = this.handleTriggerClick.bind(this);
    this.handleTransitionEnd = this.handleTransitionEnd.bind(this);
    this.continueOpenCollapsible = this.continueOpenCollapsible.bind(this);

    // Defaults the dropdown to be closed
    if (this.props.open) {
      this.state = {
        isClosed: false,
        shouldSwitchAutoOnNextCycle: false,
        height: 'auto',
        transition: 'none',
        hasBeenOpened: true,
        overflow: this.props.overflowWhenOpen,
        inTransition: false,
      }
    } else {
      this.state = {
        isClosed: true,
        shouldSwitchAutoOnNextCycle: false,
        height: 0,
        transition: `height ${this.props.transitionTime}ms ${this.props.easing}`,
        hasBeenOpened: false,
        overflow: 'hidden',
        inTransition: false,
      }
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if(this.state.shouldOpenOnNextCycle){
      this.continueOpenCollapsible();
    }

    if (prevState.height === 'auto' && this.state.shouldSwitchAutoOnNextCycle === true) {
      window.setTimeout(() => { // Set small timeout to ensure a true re-render
        this.setState({
          height: 0,
          overflow: 'hidden',
          isClosed: true,
          shouldSwitchAutoOnNextCycle: false,
        });
      }, 50);
    }

    // If there has been a change in the open prop (controlled by accordion)
    if (prevProps.open !== this.props.open) {
      if(this.props.open === true) {
        this.openCollapsible();
      } else {
        this.closeCollapsible();
      }
    }
  }

  closeCollapsible() {
    this.setState({
      shouldSwitchAutoOnNextCycle: true,
      height: this.refs.inner.offsetHeight,
      transition: `height ${this.props.transitionTime}ms ${this.props.easing}`,
      inTransition: true,
    });
  }

  openCollapsible() {
    this.setState({
      inTransition: true,
      shouldOpenOnNextCycle: true,
    });
  }

  continueOpenCollapsible() {
    this.setState({
      height: this.refs.inner.offsetHeight,
      transition: `height ${this.props.transitionTime}ms ${this.props.easing}`,
      isClosed: false,
      hasBeenOpened: true,
      inTransition: true,
      shouldOpenOnNextCycle: false,
    });
  }

  handleTriggerClick(event) {
    event.preventDefault();

    if (this.props.triggerDisabled) {
      return
    }

    if (this.props.handleTriggerClick) {
      this.props.handleTriggerClick(this.props.accordionPosition);
    } else {
      if (this.state.isClosed === true) {
        this.openCollapsible();
        this.props.onOpening();
      } else {
        this.closeCollapsible();
        this.props.onClosing();
      }
    }
  }

  renderNonClickableTriggerElement() {
    if (this.props.triggerSibling && typeof this.props.triggerSibling === 'string') {
      return (
        <span className={`${this.props.classParentString}__trigger-sibling`}>{this.props.triggerSibling}</span>
      )
    } else if(this.props.triggerSibling) {
      return <this.props.triggerSibling />
    }

    return null;
  }

  handleTransitionEnd() {
    // Switch to height auto to make the container responsive
    if (!this.state.isClosed) {
      this.setState({ height: 'auto', inTransition: false });
      this.props.onOpen();
    } else {
      this.setState({ inTransition: false });
      this.props.onClose();
    }
  }

  render() {
    let dropdownStyle = {
      height: this.state.height,
      WebkitTransition: this.state.transition,
      msTransition: this.state.transition,
      transition: this.state.transition,
      overflow: this.state.overflow,
    };

    let openClass = this.state.isClosed ? 'is-closed' : 'is-open';
    let disabledClass = this.props.triggerDisabled ? 'is-disabled' : '';

    //If user wants different text when tray is open
    let trigger = (this.state.isClosed === false) && (this.props.triggerWhenOpen !== undefined)
                  ? this.props.triggerWhenOpen
                  : this.props.trigger;

    // Don't render children until the first opening of the Collapsible if lazy rendering is enabled
    let children = (this.state.isClosed && !this.state.inTransition) ? null : this.props.children;

    // Construct CSS classes strings
    const triggerClassString = `${this.props.classParentString}__trigger ${openClass} ${disabledClass} ${
      this.state.isClosed ? this.props.triggerClassName : this.props.triggerOpenedClassName
    }`;
    const parentClassString = `${this.props.classParentString} ${
      this.state.isClosed ? this.props.className : this.props.openedClassName
    }`;
    const outerClassString = `${this.props.classParentString}__contentOuter ${this.props.contentOuterClassName}`;
    const innerClassString = `${this.props.classParentString}__contentInner ${this.props.contentInnerClassName}`;
    const plusMinusString = `fa ${this.state.isClosed ? "fa-plus" : "fa-minus"}`;

    return(
      <div className={parentClassString.trim()}>
        <div className={triggerClassString.trim()} onClick={this.handleTriggerClick}>
          <h2>{trigger}</h2>
          <div className="plus-minus-symbol" >
            <a href="javascript:void(0);" className="plus-minus-symbol-click"><i className={plusMinusString.trim()} /></a>
          </div>
          <div className="clearfix" />
        </div>

        <div 
          className={outerClassString.trim()} 
          ref="outer" 
          style={dropdownStyle}
          onTransitionEnd={this.handleTransitionEnd}
        >
          <div
            className={innerClassString.trim()}
            ref="inner"
          >
            {children}
          </div>
        </div>
      </div>
    );
  }
}

VzCollapsible.propTypes = {
  transitionTime: PropTypes.number,
  easing: PropTypes.string,
  open: PropTypes.bool,
  classParentString: PropTypes.string,
  openedClassName: PropTypes.string,
  triggerClassName: PropTypes.string,
  triggerOpenedClassName: PropTypes.string,
  contentOuterClassName: PropTypes.string,
  contentInnerClassName: PropTypes.string,
  accordionPosition: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  handleTriggerClick: PropTypes.func,
  onOpen: PropTypes.func,
  onClose: PropTypes.func,
  onOpening: PropTypes.func,
  onClosing: PropTypes.func,
  trigger: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element
  ]),
  triggerWhenOpen:PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element
  ]),
  triggerDisabled: PropTypes.bool,
  lazyRender: PropTypes.bool,
  overflowWhenOpen: PropTypes.oneOf([
    'hidden',
    'visible',
    'auto',
    'scroll',
    'inherit',
    'initial',
    'unset',
  ]),
  triggerSibling: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.func,
  ]),
};

VzCollapsible.defaultProps = {
  transitionTime: 400,
  easing: 'linear',
  open: false,
  classParentString: 'VzCollapsible',
  triggerDisabled: false,
  lazyRender: false,
  overflowWhenOpen: 'hidden',
  openedClassName: '',
  triggerClassName: '',
  triggerOpenedClassName: '',
  contentOuterClassName: '',
  contentInnerClassName: '',
  className: '',
  triggerSibling: null,
  onOpen: () => {},
  onClose: () => {},
  onOpening: () => {},
  onClosing: () => {},
};

export function VzLinkButton(props) {
  return (
    <Link to={props.to} className="btn btn-primary"><span>{props.children}</span></Link>
  )
}

export class VzModal extends React.Component {
  render() {
    if (!this.props.isOpen) {
      return null
    }

    const handleBackgroundClick = e => {
      if (e.target === e.currentTarget) this.props.hideModal()
    };

    const onOk = () => {
      this.props.onOk();
      this.props.hideModal()
    };

    const onCancel = () => {
      this.props.onCancel && this.props.onCancel();
      this.props.hideModal()
    }

    const onExtra = () => {
      this.props.onExtra();
      this.props.hideModal()
    };

    return (
      <div onClick={handleBackgroundClick}>
        <div className="ngdialog ngdialog-theme-default ng-scope">
          <div className="ngdialog-overlay" />
          <div>
            <div className="deletefolder-cabitpopup files-show-popup" id="deletefolderpopup">
              <h2>{this.props.title}</h2>
              <div className="col-md-12">     
                <div className="form-group signature-div">
                  <label><strong>{this.props.message}</strong></label>
                  <div className="clearfix"> </div>
              </div>
            </div>
            <div className="select-options">
              <div className="update-org">
                <a className="cancel-selection cabinet-btn-close" onClick={onCancel}>Cancel</a>
                { this.props.onExtra && <a className="spacer-right5 cancel-selection cabinet-btn-close" onClick={onExtra}>{this.props.extraText ? this.props.extraText : 'No'}</a>}
                <button className="change-organisation cabinet-btn-close" onClick={onOk}>{this.props.okText ? this.props.okText : 'Ok'}</button>
              </div>
            </div>
            <a onClick={this.props.onCancel} className="cabinet-close" />
          </div>
        </div>
      </div>
    </div>
    )
  }
}

VzModal.propTypes = {
  onOk: PropTypes.func.isRequired,
  isOpen: PropTypes.bool,
  children: PropTypes.node
};
