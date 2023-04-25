import { useEffect, useState } from 'react';
import Xarrow, { useXarrow, Xwrapper } from 'react-xarrows';
import data from '../../test.json';
function App() {
  // States
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [pheromone_lines, setPheromone_lines] = useState([]);
  const [current_path, setCurrent_path] = useState();
  const [current_path_ghost, setCurrent_path_ghost] = useState();
  const [ghostLines, setGhostLines] = useState(false);
  const [points, setPoints] = useState([]);
  const [chargers, setChargers] = useState([]);
  const [maxX, setMaxX] = useState(0);
  const [maxY, setMaxY] = useState(0);
  const [minX, setMinX] = useState(0);
  const [minY, setMinY] = useState(0);
  const [lastTakenPath, setLastTakenPath] = useState();
  const [PIntensity, setPIntensity] = useState(0);
  // const [pheromone_matrix, setPheromone_matrix] = useState([]);
  // const [pheromone_updates, setPheromone_updates] = useState([]);
  // const [all_paths, setAll_paths] = useState([]);

  useEffect(() => {
    setPoints(data.points);
    setChargers(data.chargers);
    setLoading(false);

    const allpoints = data.points.concat(data.chargers);
    let mx = 0;
    let my = 0;
    for (let i = 0; i < allpoints.length; i++) {
      if (allpoints[i][0] > mx) {
        mx = allpoints[i][0];
      }
      if (allpoints[i][1] > my) {
        my = allpoints[i][1];
      }
    }
    setMaxX(mx);
    setMaxY(my);
    let minx = mx;
    let miny = my;
    for (let i = 0; i < allpoints.length; i++) {
      if (allpoints[i][0] < minx) {
        minx = allpoints[i][0];
      }
      if (allpoints[i][1] < miny) {
        miny = allpoints[i][1];
      }
    }
    setMinX(minx);
    setMinY(miny);
    setPIntensity(data.PHEROMONE_INTENSITY);
  }, []);

  function drawPheromoneMap() {
    let new_map = pheromone_lines;
    // if (new_map.length === 0) {
    //   data.pheromone_updates[currentIndex].forEach((update, index) => {
    //     new_map.push(createPheromoneLine(update[0], update[1], update[2]));
    //   });
    // }

    data.pheromone_updates[currentIndex].forEach((update, index) => {
      let new_line = true;
      for (let i = 0; i < new_map.length; i++) {
        if (new_map[i][0] === update[0] && new_map[i][1] === update[1]) {
          new_map[i] = [update[0], update[1], update[2]];
          new_line = false;
        } else if (new_map[i][0] === update[1] && new_map[i][1] === update[0]) {
          new_map[i] = [update[0], update[1], update[2]];
          new_line = false;
        }
      }
      if (new_line) {
        new_map.push([update[0], update[1], update[2]]);
      }
    });
    if (currentIndex === 0) {
      data.pheromone_updates[currentIndex].forEach((update, index) => {
        new_map.push([update[0], update[1], update[2]]);
      });
    }
    setPheromone_lines(new_map);
  }

  function createPheromoneLine(n1, n2, weight, index) {
    return (
      <Xarrow
        key={`ph-${n1}-${n2}-${index}`}
        start={`p-node-${n1}`}
        end={`p-node-${n2}`}
        // startAnchor="auto"
        // endAnchor="auto"
        color="red"
        showHead={false}
        headSize={4}
        strokeWidth={(weight / PIntensity) * 30}
        path={'straight'}
        startAnchor='middle'
        endAnchor={'middle'}
        showXarrow={true}
        // curveness={false}
        // animateDrawing={1 * i}
      />
    );
  }

  function handleNewPath() {
    let currentPath = data.final_paths[currentIndex];

    let currentPathLines = [];
    for (let i = 0; i < currentPath.length - 1; i++) {
      currentPathLines.push(
        <Xarrow
          key={`path-${i}`}
          start={`node-${currentPath[i]}`}
          end={`node-${currentPath[i + 1]}`}
          startAnchor="auto"
          endAnchor="auto"
          showHead={true}
          headSize={8}
          color="black"
          // labels={<div className="text-[0.7rem]">Move {i + 1}</div>}
          strokeWidth={1}
          path="straight"
          showXarrow={true}
          // curveness={false}
          // animateDrawing={1 * i}
        />
      );
    }
    setCurrent_path(currentPathLines);

    let currentPathGhost = data.final_paths[currentIndex];

    let currentPathGhostLines = [];
    for (let i = 0; i < currentPathGhost.length - 1; i++) {
      currentPathGhostLines.push(
        <Xarrow
          key={`pathGhost-${i}`}
          start={`p-node-${currentPath[i]}`}
          end={`p-node-${currentPath[i + 1]}`}
          startAnchor="middle"
          endAnchor="middle"
          showHead={true}
          headSize={8}
          color="black"
          // labels={<div className="text-[0.7rem]">Move {i + 1}</div>}
          strokeWidth={1}
          path="straight"
          showXarrow={true}
          // curveness={false}
          // animateDrawing={1 * i}
        />
      );
    }
    setCurrent_path_ghost(currentPathGhostLines);

    let pathString = '';
    data.final_paths[currentIndex].forEach((move) => {
      pathString = pathString + move + '->';
    });

    setLastTakenPath(pathString.slice(0, -2));
  }

  function normalize(value, n) {
    const range = (maxX > maxY ? maxX : maxY) + 6 - (minX < minY ? minX : minY);
    // console.log(`minX= ${minX}`);
    // console.log(`minY= ${minY}`);
    // console.log(`maxX= ${maxX}`);
    // console.log(`maxY= ${maxY}`);
    // console.log(`range= ${range}`);

    return ((value - (minX < minY ? minX : minY)) / range) * n - 6 + 25;
  }

  const scalePositions = 3;
  const boxSize = 500;
  return loading ? (
    <div>Loading</div>
  ) : (
    <div className="flex flex-col items-center justify-center h-screen gap-5">
      <div className="text-3xl max-w-[1000px] min-h-[120px]">
        ({currentIndex})Path: {lastTakenPath}
      </div>
      <div className="App flex items-center justify-center h-fit gap-6">
        <Xwrapper className="">
          <div className="">
            <p className="">Path taken</p>
            <div className="relative top-0 left-0">
              <div
                className={`border border-black w-[550px] h-[550px] top-0 left-0`}
              >
                {points.map((point, index) => (
                  <div
                    key={index}
                    className={`node point node-${index}`}
                    id={`node-${index}`}
                    style={{
                      position: 'absolute',
                      margin: '0px',
                      left: `${normalize(point[0], boxSize)}px`,
                      top: `${normalize(point[1], boxSize)}px`,
                    }}
                  >
                    {index}
                  </div>
                ))}
                {chargers.map((charger, index) => (
                  <div
                    key={index}
                    className={`node charger node-${-index - 1}`}
                    id={`node-${-index - 1}`}
                    style={{
                      position: 'absolute',
                      margin: '0px',
                      left: `${normalize(charger[0], boxSize)}px`,
                      top: `${normalize(charger[1], boxSize)}px`,
                    }}
                  >
                    {-index - 1}
                  </div>
                ))}
                {current_path}
              </div>
            </div>
          </div>

          <div>
            <div className="flex gap-10 items-center">
              <p>Pheromone Map</p>
              <button
                className=""
                onMouseEnter={() => setGhostLines(!ghostLines)}
                onMouseLeave={() => setGhostLines(!ghostLines)}
                onClick={() => setGhostLines(!ghostLines)}
              >
                Toggle Path Overlay
              </button>
            </div>
            <div className={`border border-black relative w-[550px] h-[550px]`}>
              {points.map((point, index) => (
                <div
                  key={index}
                  className={`node point node-${index}`}
                  id={`p-node-${index}`}
                  style={{
                    position: 'absolute',
                    margin: '0px',
                    left: `${normalize(point[0], boxSize)}px`,
                    top: `${normalize(point[1], boxSize)}px`,
                  }}
                >
                  {index}
                </div>
              ))}
              {chargers.map((charger, index) => (
                <div
                  key={index}
                  className={`node charger node-${-index - 1}`}
                  id={`p-node-${-index - 1}`}
                  style={{
                    position: 'absolute',
                    margin: '0px',
                    left: `${normalize(charger[0], boxSize)}px`,
                    top: `${normalize(charger[1], boxSize)}px`,
                  }}
                >
                  {-index - 1}
                </div>
              ))}
              {pheromone_lines.map((line, index) =>
                createPheromoneLine(line[0], line[1], line[2], index)
              )}
              {ghostLines ? current_path_ghost : <></>}
            </div>
          </div>
        </Xwrapper>
      </div>
      <button
        onClick={() => {
          handleNewPath();
          drawPheromoneMap();
          setCurrentIndex(currentIndex + 1);
        }}
        className="btn"
      >
        move
      </button>
    </div>
  );
}

export default App;
