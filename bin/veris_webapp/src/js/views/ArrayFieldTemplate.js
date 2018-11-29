import React from 'react';

function ArrayItem(props) {
  return (
    <div key={props.index} className={props.className}>
      <div className="col-xs-10">
        {props.children}
      </div>
      <div className="col-xs-2 text-right">
        {props.hasRemove && (
              <button
                type="danger"
                icon="remove"
                className="btn btn-secondary btn-radius"
                tabIndex="-1"
                disabled={props.disabled || props.readonly}
                onClick={props.onDropIndexClick(props.index)}
              >Remove</button>
            )}
      </div>
      <div className="clearfix" />
    </div>
  )
}

export default function ArrayFieldTemplate(props) {
  const {
    idSchema,
    title
  } = props;

  return(
    <div>
      <div className="col-xs-10">
        <legend id={`${idSchema.$id}__title`}>{title}</legend>
      </div>
      <div className="col-xs-2 text-right">
        {props.canAdd && <button type="submit" className="btn btn-primary btn-radius spacer10" onClick={props.onAddClick}>Add</button>}
      </div>
      <div className="clearfix" />
      {props.items.map(ArrayItem)}
    </div>
  )
}