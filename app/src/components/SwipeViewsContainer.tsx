import { styled } from "@mui/material";
import { Children, PropsWithChildren } from "react";

export default function SwipeViewsContainer(props: PropsWithChildren<{ currentIndex: number }>) {
	return <SContainer>
		{
			Children.map(props.children, (child, index) => {
				let offset = Math.sign(index - props.currentIndex);

				return <div
					key={index}
					children={child}
					style={{
						transform: offset === 0 ? 'none' : `translateX(calc(100% * ${offset}))`,
						pointerEvents: offset === 0 ? 'inherit' : 'none',
						opacity: offset === 0 ? 1 : 0,
					}}
				/>
			})
		}
	</SContainer>
}

const SContainer = styled('div')`
	display: grid;
	overflow-x: hidden;
	> div {
		grid-area: 1/1;
		transition: opacity ease 300ms, transform ease 300ms;
	}
`;