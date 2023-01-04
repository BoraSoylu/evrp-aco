import React from 'react';
export const ACOSettingsPanel = () => {
  return (
    <div className="border w-fit rounded p-2 shadow shadow-gray-700">
      <form className="w-fit grid grid-cols-1 sm:grid-flow-col-1 md:grid-cols-2 xl:grid-cols-2">
        <div className="settings-label-input-wrapper">
          <label htmlFor="" className="settings-input-label">
            Number of Drop-off Nodes
          </label>
          <input
            type="text"
            name=""
            id=""
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="" className="settings-input-label">
            Number of Charger Nodes
          </label>
          <input
            type="text"
            name=""
            id=""
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="scout-ant-count" className="settings-input-label">
            Scout Ants
          </label>
          <input
            type="text"
            name="scout-ant-count"
            id="scout-ant-count"
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="main-ant-count" className="settings-input-label">
            Main Ants
          </label>
          <input
            type="text"
            name="main-ant-count"
            id="main-ant-count"
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="" className="settings-input-label">
            Max Battery
          </label>
          <input
            type="text"
            name=""
            id=""
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="" className="settings-input-label">
            Battery Drain Per Distance
          </label>
          <input
            type="text"
            name=""
            id=""
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="" className="settings-input-label">
            Min Allowed Battery
          </label>
          <input
            type="text"
            name=""
            id=""
            autoComplete=""
            className="settings-input"
          />
        </div>
        <div className="settings-label-input-wrapper">
          <label htmlFor="" className="settings-input-label">
            Pheromone Evaporation Rate
          </label>
          <input
            type="text"
            name=""
            id=""
            autoComplete=""
            className="settings-input"
          />
        </div>
      </form>
    </div>
  );
};
