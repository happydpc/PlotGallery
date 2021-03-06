Point(0) = {0.000000, 0.000000, 0.000000};
Point(1) = {8.000000, 0.000000, 0.000000};
Point(2) = {22.000000, 12.000000, 0.000000};
Point(3) = {109.000000, 13.518591, 0.000000};
Point(4) = {115.000000, 13.623321, 0.000000};
Point(5) = {115.000000, 27.623321, 0.000000};
Point(6) = {44.500800, 63.398400, 0.000000};
Point(7) = {22.000000, 73.000000, 0.000000};
Point(8) = {12.496800, 28.346400, 0.000000};
Point(9) = {14.000000, 98.000000, 0.000000};
Point(10) = {2.000000, 110.000000, 0.000000};
Point(11) = {0.000000, 110.000000, 0.000000};
Line(12) = {1,0};
Line(13) = {2,1};
Line(14) = {3,2};
Line(15) = {4,3};
Line(16) = {5,4};
Circle(17) = {7, 6, 5};
Circle(18) = {9, 8, 7};
Line(19) = {10,9};
Line(20) = {11,10};
Line(21) = {0,11};
Line Loop(22) = {21,20,19,18,17,16,15,14,13,12};
Plane Surface(23) = {22};
Physical Surface('A0') = {23};
Physical Surface('PART0') = {23};
Physical Line('L0') = {12};
Physical Line('L1') = {13};
Physical Line('L2') = {14};
Physical Line('L3') = {15};
Physical Line('L4') = {16};
Physical Line('L5') = {17};
Physical Line('L6') = {18};
Physical Line('L7') = {19};
Physical Line('L8') = {20};
Physical Line('L9') = {21};
Physical Point('P0') = {0};
Physical Point('P1') = {1};
Physical Point('P2') = {2};
Physical Point('P3') = {3};
Physical Point('P4') = {4};
Physical Point('P5') = {5};
Physical Point('P6') = {6};
Physical Point('P7') = {7};
Physical Point('P8') = {8};
Physical Point('P9') = {9};
Physical Point('P10') = {10};
Physical Point('P11') = {11};
Mesh.RecombinationAlgorithm = 1; //blossom
Mesh.RecombineAll = 1; //turns on quads
Mesh.SubdivisionAlgorithm = 1; // quadrangles only
Mesh.CharacteristicLengthExtendFromBoundary = 1;
Mesh.CharacteristicLengthMin = 0;
Mesh.CharacteristicLengthMax = 1e+022;
Mesh.CharacteristicLengthFromPoints = 1;
Mesh.Algorithm = 8; //delquad = delauny for quads
Mesh.ElementOrder = 2; //linear or second set here
Mesh.SecondOrderIncomplete=1; //no face node w/ 2nd order
Mesh.SaveGroupsOfNodes = 1; // save node groups
