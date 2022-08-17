"use strict";
var __spreadArray = (this && this.__spreadArray) || function (to, from) {
    for (var i = 0, il = from.length, j = to.length; i < il; i++, j++)
        to[j] = from[i];
    return to;
};
var framework;
(function (framework) {
    var FileParser = /** @class */ (function () {
        function FileParser(filename, content) {
            this.filename = filename;
            this.content = [];
            for (var _i = 0, _a = content.trim().split('\n'); _i < _a.length; _i++) {
                var line = _a[_i];
                var words = line.trim().split(new RegExp('\\s+'));
                this.content.push(words);
            }
            this.y = 0;
            this.x = 0;
        }
        FileParser.prototype.isEOF = function () {
            return this.content.length <= this.y;
        };
        FileParser.prototype.isNewLine = function () {
            return this.y < this.content.length && this.x === this.content[this.y].length;
        };
        FileParser.prototype.getWord = function () {
            if (this.isEOF()) {
                this.reportError('a word expected, but EOF');
            }
            if (this.content[this.y].length <= this.x) {
                this.reportError('a word expected, but newline');
            }
            var word = this.content[this.y][this.x];
            this.x += 1;
            return word;
        };
        FileParser.prototype.getInt = function () {
            var word = this.getWord();
            if (!word.match(new RegExp('^[-+]?[0-9]+$'))) {
                this.reportError("a number expected, but word " + JSON.stringify(this.content[this.y][this.x]));
            }
            return parseInt(word);
        };
        FileParser.prototype.getNewline = function () {
            if (this.isEOF()) {
                this.reportError('newline expected, but EOF');
            }
            if (this.x < this.content[this.y].length) {
                this.reportError("newline expected, but word " + JSON.stringify(this.content[this.y][this.x]));
            }
            this.x = 0;
            this.y += 1;
        };
        FileParser.prototype.reportError = function (msg) {
            msg = this.filename + ": line " + (this.y + 1) + ": " + msg;
            alert(msg);
            throw new Error(msg);
        };
        return FileParser;
    }());
    framework.FileParser = FileParser;
    var FileSelector = /** @class */ (function () {
        function FileSelector(callback) {
            var _this = this;
            this.callback = callback;
            this.inputFile = document.getElementById("inputFile");
            this.outputFile = document.getElementById("outputFile");
            this.reloadButton = document.getElementById("reloadButton");
            this.reloadFilesClosure = function () {
                _this.reloadFiles();
            };
            this.inputFile.addEventListener('change', this.reloadFilesClosure);
            this.outputFile.addEventListener('change', this.reloadFilesClosure);
            this.reloadButton.addEventListener('click', this.reloadFilesClosure);
            this.inputFile.addEventListener('click', function () {
                _this.inputFile.value = "";
            });
            this.outputFile.addEventListener('click', function () {
                _this.outputFile.value = "";
            });
        }
        FileSelector.prototype.reloadFiles = function () {
            var _this = this;
            if (this.inputFile.files == null || this.inputFile.files.length == 0)
                return;
            loadFile(this.inputFile.files[0], function (inputContent) {
                if (_this.outputFile.files == null || _this.outputFile.files.length == 0)
                    return;
                loadFile(_this.outputFile.files[0], function (outputContent) {
                    _this.reloadButton.classList.remove('disabled');
                    if (_this.callback !== undefined) {
                        _this.callback(inputContent, outputContent);
                    }
                });
            });
        };
        return FileSelector;
    }());
    framework.FileSelector = FileSelector;
    var RichSeekBar = /** @class */ (function () {
        function RichSeekBar(callback) {
            var _this = this;
            this.callback = callback;
            this.seekRange = document.getElementById("seekRange");
            this.seekNumber = document.getElementById("seekNumber");
            this.fpsInput = document.getElementById("fpsInput");
            this.firstButton = document.getElementById("firstButton");
            this.prevButton = document.getElementById("prevButton");
            this.playButton = document.getElementById("playButton");
            this.nextButton = document.getElementById("nextButton");
            this.lastButton = document.getElementById("lastButton");
            this.runIcon = document.getElementById("runIcon");
            this.intervalId = null;
            this.setMinMax(-1, -1);
            this.seekRange.addEventListener('change', function () {
                _this.setValue(parseInt(_this.seekRange.value));
            });
            this.seekNumber.addEventListener('change', function () {
                _this.setValue(parseInt(_this.seekNumber.value));
            });
            this.seekRange.addEventListener('input', function () {
                _this.setValue(parseInt(_this.seekRange.value));
            });
            this.seekNumber.addEventListener('input', function () {
                _this.setValue(parseInt(_this.seekNumber.value));
            });
            this.fpsInput.addEventListener('change', function () {
                if (_this.intervalId !== null) {
                    _this.play();
                }
            });
            this.firstButton.addEventListener('click', function () {
                _this.stop();
                _this.setValue(_this.getMin());
            });
            this.prevButton.addEventListener('click', function () {
                _this.stop();
                _this.setValue(_this.getValue() - 1);
            });
            this.nextButton.addEventListener('click', function () {
                _this.stop();
                _this.setValue(_this.getValue() + 1);
            });
            this.lastButton.addEventListener('click', function () {
                _this.stop();
                _this.setValue(_this.getMax());
            });
            this.playClosure = function () {
                _this.play();
            };
            this.stopClosure = function () {
                _this.stop();
            };
            this.playButton.addEventListener('click', this.playClosure);
        }
        RichSeekBar.prototype.setMinMax = function (min, max) {
            this.seekRange.min = this.seekNumber.min = min.toString();
            this.seekRange.max = this.seekNumber.max = max.toString();
            this.seekRange.step = this.seekNumber.step = '1';
            this.setValue(min);
        };
        RichSeekBar.prototype.getMin = function () {
            return parseInt(this.seekRange.min);
        };
        RichSeekBar.prototype.getMax = function () {
            return parseInt(this.seekRange.max);
        };
        RichSeekBar.prototype.setValue = function (value) {
            value = Math.max(this.getMin(), Math.min(this.getMax(), value)); // clamp
            var preValue = this.seekNumber.valueAsNumber;
            this.seekRange.value = this.seekNumber.value = value.toString();
            if (this.callback !== undefined) {
                this.callback(value, preValue);
            }
        };
        RichSeekBar.prototype.getValue = function () {
            return parseInt(this.seekRange.value);
        };
        RichSeekBar.prototype.getDelay = function () {
            var fps = parseInt(this.fpsInput.value);
            return Math.floor(1000 / fps);
        };
        RichSeekBar.prototype.resetInterval = function () {
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
        };
        RichSeekBar.prototype.play = function () {
            var _this = this;
            this.playButton.removeEventListener('click', this.playClosure);
            this.playButton.addEventListener('click', this.stopClosure);
            this.runIcon.classList.remove('play');
            this.runIcon.classList.add('stop');
            if (this.getValue() == this.getMax()) { // if last, go to first
                this.setValue(this.getMin());
            }
            this.resetInterval();
            this.intervalId = setInterval(function () {
                if (_this.getValue() == _this.getMax()) {
                    _this.stop();
                }
                else {
                    _this.setValue(_this.getValue() + 1);
                }
            }, this.getDelay());
        };
        RichSeekBar.prototype.stop = function () {
            this.playButton.removeEventListener('click', this.stopClosure);
            this.playButton.addEventListener('click', this.playClosure);
            this.runIcon.classList.remove('stop');
            this.runIcon.classList.add('play');
            this.resetInterval();
        };
        return RichSeekBar;
    }());
    framework.RichSeekBar = RichSeekBar;
    var loadFile = function (file, callback) {
        var reader = new FileReader();
        reader.readAsText(file);
        reader.onloadend = function () {
            if (typeof reader.result == 'string')
                callback(reader.result);
        };
    };
    var saveUrlAsLocalFile = function (url, filename) {
        var anchor = document.createElement('a');
        anchor.href = url;
        anchor.download = filename;
        var evt = document.createEvent('MouseEvent');
        evt.initEvent("click", true, true);
        anchor.dispatchEvent(evt);
    };
    var FileExporter = /** @class */ (function () {
        function FileExporter(canvas) {
            var saveAsImage = document.getElementById("saveAsImage");
            saveAsImage.addEventListener('click', function () {
                saveUrlAsLocalFile(canvas.toDataURL('image/png'), 'canvas.png');
            });
        }
        return FileExporter;
    }());
    framework.FileExporter = FileExporter;
})(framework || (framework = {}));
var visualizer;
(function (visualizer) {
    function isInside(value, min, max) {
        return min <= value && value <= max;
    }
    var Vege = /** @class */ (function () {
        function Vege(R, C, S, E, V) {
            this.R = R;
            this.C = C;
            this.S = S;
            this.E = E;
            this.V = V;
        }
        return Vege;
    }());
    var InputFile = /** @class */ (function () {
        function InputFile(content) {
            this.veges = [];
            var parser = new framework.FileParser('<input-file>', content);
            this.N = parser.getInt();
            this.M = parser.getInt();
            this.T = parser.getInt();
            parser.getNewline();
            for (var i = 0; i < this.M; i++) {
                var r = parser.getInt();
                var c = parser.getInt();
                var s = parser.getInt();
                var t = parser.getInt();
                var v = parser.getInt();
                parser.getNewline();
                this.veges.push(new Vege(r, c, s, t, v));
            }
        }
        return InputFile;
    }());
    var OutputFile = /** @class */ (function () {
        function OutputFile(content, inputFile) {
            this.commands = [];
            var parser = new framework.FileParser('<output-file>', content);
            var rows = content.trim().split("\n");
            if (rows.length !== inputFile.T) {
                var msg = "<output-file> invalid number of lines";
                alert(msg);
                throw new Error(msg);
            }
            for (var i = 0; i < inputFile.T; i++) {
                var command = [];
                while (!parser.isEOF() && !parser.isNewLine()) {
                    command.push(parser.getInt());
                }
                if (command.length === 1) {
                    if (command[0] !== -1) {
                        parser.reportError("invalid output");
                    }
                }
                else if (command.length === 2) {
                    if (command.some(function (v) { return !isInside(v, 0, inputFile.N - 1); })) {
                        parser.reportError("value out of range");
                    }
                }
                else if (command.length === 4) {
                    if (command.some(function (v) { return !isInside(v, 0, inputFile.N - 1); })) {
                        parser.reportError("value out of range");
                    }
                }
                else {
                    parser.reportError("invalid output");
                }
                this.commands.push(command);
                if (i < inputFile.T) {
                    parser.getNewline();
                }
            }
            if (!parser.isEOF()) {
                parser.reportError("too many output");
            }
        }
        return OutputFile;
    }());
    var TesterFrame = /** @class */ (function () {
        function TesterFrame(turn, money, price, command, values, machines, log) {
            this.turn = turn;
            this.money = money;
            this.price = price;
            this.command = command;
            this.values = values;
            this.machines = machines;
            this.log = log;
        }
        return TesterFrame;
    }());
    var Tester = /** @class */ (function () {
        function Tester(inputContent, outputContent) {
            function error(row, msg) {
                msg = "<output-file>: line " + (row + 1) + ": " + msg;
                alert(msg);
                throw new Error(msg);
            }
            var input = new InputFile(inputContent);
            var output = new OutputFile(outputContent, input);
            var money = 1;
            var next_price = 1;
            var num_machine = 0;
            var values = new Array(input.N);
            var machines = new Array(input.N);
            for (var i = 0; i < input.N; i++) {
                values[i] = new Array(input.N).fill(0);
                machines[i] = new Array(input.N).fill(false);
            }
            var vege_start = new Array(input.T);
            var vege_end = new Array(input.T);
            for (var i = 0; i < input.T; i++) {
                vege_start[i] = [];
                vege_end[i] = [];
            }
            input.veges.forEach(function (vege) {
                vege_start[vege.S].push(vege);
                vege_end[vege.E].push(vege);
            });
            this.frames = [];
            var _loop_1 = function (i) {
                var command = output.commands[i];
                var log = [];
                if (command.length === 2) {
                    if (money < next_price) {
                        error(i, "your money is not sufficient to purchase");
                    }
                    if (machines[command[0]][command[1]]) {
                        error(i, "specified position already has a machine");
                    }
                    log.push("spent " + next_price + " to purchase");
                    money -= next_price;
                    machines[command[0]][command[1]] = true;
                    num_machine++;
                    next_price = Math.pow(num_machine + 1, 3);
                }
                else if (command.length === 4) {
                    if (!machines[command[0]][command[1]]) {
                        error(i, "move start position doesn't have a machine");
                    }
                    if ((command[0] !== command[2] || command[1] !== command[3]) && machines[command[2]][command[3]]) {
                        error(i, "move end position already has a machine");
                    }
                    machines[command[0]][command[1]] = false;
                    machines[command[2]][command[3]] = true;
                }
                vege_start[i].forEach(function (vege) {
                    values[vege.R][vege.C] = vege.V;
                });
                // harvest
                var DR = [1, 0, -1, 0];
                var DC = [0, 1, 0, -1];
                var con_size = new Array(input.N).fill(0).map(function (_) { return new Array(input.N).fill(0); });
                for (var r = 0; r < input.N; r++) {
                    var _loop_2 = function (c) {
                        if (!machines[r][c] || con_size[r][c] !== 0)
                            return "continue";
                        var q = [[r, c]];
                        con_size[r][c] = -1;
                        var qi = 0;
                        while (qi < q.length) {
                            var cr = q[qi][0];
                            var cc = q[qi][1];
                            for (var dir = 0; dir < 4; dir++) {
                                var nr = cr + DR[dir];
                                var nc = cc + DC[dir];
                                if (isInside(nr, 0, input.N - 1) && isInside(nc, 0, input.N - 1) &&
                                    machines[nr][nc] && con_size[nr][nc] === 0) {
                                    q.push([nr, nc]);
                                    con_size[nr][nc] = -1;
                                }
                            }
                            qi++;
                        }
                        q.forEach(function (pos) {
                            con_size[pos[0]][pos[1]] = q.length;
                            var v = values[pos[0]][pos[1]];
                            if (v > 0) {
                                log.push("earned " + v * q.length + "=" + v + "*" + q.length + " at (" + pos[0] + "," + pos[1] + ")");
                                money += v * q.length;
                            }
                        });
                    };
                    for (var c = 0; c < input.N; c++) {
                        _loop_2(c);
                    }
                }
                this_1.frames.push(new TesterFrame(i, money, next_price, command, 
                // deep copy
                values.map(function (a) { return __spreadArray([], a); }), machines.map(function (a) { return __spreadArray([], a); }), log));
                // clear veges after visualization
                for (var r = 0; r < input.N; r++) {
                    for (var c = 0; c < input.N; c++) {
                        if (machines[r][c]) {
                            values[r][c] = 0;
                        }
                    }
                }
                vege_end[i].forEach(function (vege) {
                    values[vege.R][vege.C] = 0;
                });
            };
            var this_1 = this;
            for (var i = 0; i < input.T; i++) {
                _loop_1(i);
            }
        }
        return Tester;
    }());
    var Visualizer = /** @class */ (function () {
        function Visualizer() {
            this.canvas = document.getElementById("canvas");
            // adjust resolution
            this.dpr = window.devicePixelRatio || 1;
            var height = this.canvas.height;
            var width = this.canvas.width;
            this.canvas.style.height = height + 'px';
            this.canvas.style.width = width + 'px';
            this.height = this.canvas.height = height * this.dpr; // pixels
            this.width = this.canvas.width = width * this.dpr; // pixels
            this.offset = 10 * this.dpr; // pixels
            this.ctx = this.canvas.getContext('2d');
            if (this.ctx == null) {
                alert('unsupported browser');
            }
            this.moneyInput = document.getElementById("moneyInput");
            this.actionInput = document.getElementById("actionInput");
            this.machinesInput = document.getElementById("machinesInput");
            this.priceInput = document.getElementById("priceInput");
            this.logArea = document.getElementById("logArea");
            this.ctx.lineJoin = 'round';
            this.ctx.font = 18 * this.dpr + "px sans-serif";
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
        }
        Visualizer.prototype.draw = function (frame) {
            var N = frame.values.length;
            var num_machine = 0;
            for (var i = 0; i < N; i++) {
                for (var j = 0; j < N; j++) {
                    if (frame.machines[i][j]) {
                        num_machine++;
                    }
                }
            }
            this.moneyInput.value = frame.money.toString();
            this.actionInput.value = frame.command.join(" ");
            this.machinesInput.value = num_machine.toString();
            this.priceInput.value = frame.price.toString();
            this.logArea.value = frame.log.join("\n");
            var cellSize = (Math.min(this.height, this.width) - this.offset * 2) / N;
            var offsetY = (this.height - cellSize * N) / 2;
            var offsetX = (this.width - cellSize * N) / 2;
            this.ctx.fillStyle = "#dfffdf";
            this.ctx.fillRect(0, 0, this.width, this.height);
            this.ctx.translate(offsetX, offsetY);
            // machine
            var lineWidth = 4;
            this.ctx.strokeStyle = "#b8860b";
            this.ctx.lineWidth = lineWidth;
            this.ctx.fillStyle = "#5fff5f";
            for (var i = 0; i < N; i++) {
                for (var j = 0; j < N; j++) {
                    if (frame.machines[i][j]) {
                        if (frame.values[i][j] > 0) {
                            this.ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);
                        }
                        this.ctx.strokeRect(j * cellSize + lineWidth / 2 + 5, i * cellSize + lineWidth / 2 + 5, cellSize - lineWidth - 10, cellSize - lineWidth - 10);
                    }
                }
            }
            if (frame.command.length > 1) {
                this.ctx.strokeStyle = frame.command.length === 2 ? "#f95c2d" : "#b8860b";
                this.ctx.lineWidth = lineWidth * 2;
                var r = frame.command[frame.command.length - 2];
                var c = frame.command[frame.command.length - 1];
                this.ctx.strokeRect(c * cellSize + lineWidth, r * cellSize + lineWidth, cellSize - lineWidth * 2, cellSize - lineWidth * 2);
            }
            if (frame.command.length === 4) {
                this.ctx.strokeStyle = "#d7e7b5";
                this.ctx.lineWidth = lineWidth;
                var r = frame.command[0];
                var c = frame.command[1];
                this.ctx.strokeRect(c * cellSize + lineWidth / 2 + 5, r * cellSize + lineWidth / 2 + 5, cellSize - lineWidth - 10, cellSize - lineWidth - 10);
            }
            // vegetable value
            function d2h(d) { return d.toString(16); }
            function h2d(h) { return parseInt(h, 16); }
            var from = "#000000", to = "#ff5050";
            for (var i = 0; i < N; i++) {
                for (var j = 0; j < N; j++) {
                    if (frame.values[i][j] !== 0) {
                        var weight = Math.log2(frame.values[i][j]) / 11.0;
                        var color = "#";
                        for (var i_1 = 0; i_1 < 3; i_1++) {
                            var v1 = h2d(from.substr(2 * i_1 + 1, 2));
                            var v2 = h2d(to.substr(2 * i_1 + 1, 2));
                            var v = d2h(Math.floor(v1 + (v2 - v1) * weight));
                            while (v.length < 2) {
                                v = '0' + v;
                            }
                            color += v;
                        }
                        this.ctx.fillStyle = color;
                        this.ctx.fillText(frame.values[i][j].toString(), (j + 0.5) * cellSize, (i + 0.5) * cellSize);
                    }
                }
            }
            // border
            this.ctx.strokeStyle = "#888";
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            for (var i = 0; i <= N; i++) {
                this.ctx.moveTo(0, i * cellSize);
                this.ctx.lineTo(N * cellSize, i * cellSize);
                this.ctx.moveTo(i * cellSize, 0);
                this.ctx.lineTo(i * cellSize, N * cellSize);
            }
            this.ctx.closePath();
            this.ctx.stroke();
            this.ctx.translate(-offsetX, -offsetY);
        };
        Visualizer.prototype.getCanvas = function () {
            return this.canvas;
        };
        return Visualizer;
    }());
    var App = /** @class */ (function () {
        function App() {
            var _this = this;
            this.tester = null;
            this.visualizer = new Visualizer();
            this.exporter = new framework.FileExporter(this.visualizer.getCanvas());
            this.seek = new framework.RichSeekBar(function (curValue, preValue) {
                if (_this.tester) {
                    _this.visualizer.draw(_this.tester.frames[curValue]);
                }
            });
            this.loader = new framework.FileSelector(function (inputContent, outputContent) {
                _this.tester = new Tester(inputContent, outputContent);
                _this.seek.setMinMax(0, _this.tester.frames.length - 1);
                _this.seek.setValue(0);
                _this.visualizer.draw(_this.tester.frames[0]);
            });
        }
        return App;
    }());
    visualizer.App = App;
})(visualizer || (visualizer = {}));
window.onload = function () {
    new visualizer.App();
};
//# sourceMappingURL=index.js.map